import bpy
from bpy.types import Operator
from .utils import (
    get_mouse_3d_on_grid, snap_mouse, cross2d,
    apply_offset, apply_location_line_offset, fillet_points,
    shift_polyline, build_wall_geometry, draw_dashed_line_2d
)
from bpy_extras import view3d_utils
from mathutils import Vector
from math import atan2, degrees
import gpu
from gpu_extras.batch import batch_for_shader
import blf


class CABINET_OT_draw_wall(Operator):
    bl_idname = "cabinet.draw_wall"
    bl_label = "Draw Wall"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.points = []
        self.preview_point = None
        self.wall_obj = None
        self.draw_handle = None
        self.collinear_threshold = 0.15
        self.close_threshold = 0.30
        self.is_close_loop = False
        self.wall_objects = []
        self.rect_state = 0
        self.rect_start = None

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def invoke(self, context, event):
        settings = context.scene.cabinet_tool_settings
        if settings.draw_type != 'LINE':
            self.report({'INFO'}, f"{settings.draw_type} mode — Coming Soon")
            # Still allow LINE fallback
        settings.is_drawing = True
        try:
            context.scene.cabinet_active_tool = 'DRAW_WALL'
        except:
            pass
        self.points = []
        self.wall_objects = []
        self.rect_state = 0
        self.rect_start = None

        args = (context,)
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, args, 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        settings = context.scene.cabinet_tool_settings

        if not settings.is_drawing:
            self.finish(context, keep_walls=True)
            return {'CANCELLED'}

        if event.type == 'ESC':
            self.finish(context, keep_walls=True)
            return {'CANCELLED'}

        if event.type == 'RET' and event.value == 'PRESS':
            if len(self.points) >= 2:
                self.finish_wall_segment(context, settings)
                self.points = []
                self.preview_point = None
                self.wall_obj = None
                return {'RUNNING_MODAL'}
            else:
                self.finish(context, keep_walls=True)
                return {'CANCELLED'}

        if event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
            if len(self.points) > 1:
                self.points.pop()
                self.update_mesh(context, settings)
                return {'RUNNING_MODAL'}
            else:
                self.finish(context, keep_walls=True)
                return {'CANCELLED'}

        if event.type == 'SPACE' and event.value == 'PRESS':
            settings.wall_offset_flip = not settings.wall_offset_flip
            self.update_mesh(context, settings)
            return {'RUNNING_MODAL'}

        if event.type == 'MOUSEMOVE':
            self.update_preview(context, event, settings)
            return {'PASS_THROUGH'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            snapped = self.get_snapped_pos(context, event, settings)

            if settings.draw_type == 'RECTANGLE':
                return self._handle_rectangle(context, settings, snapped)

            if not self.points:
                self.points.append(snapped)
                return {'RUNNING_MODAL'}

            if len(self.points) >= 3 and self.is_close_loop:
                self.points.append(self.points[0].copy())
                self.finish_wall_segment(context, settings)
                self.finish(context, keep_walls=True)
                return {'FINISHED'}

            self.points.append(snapped)

            if not settings.wall_chain and len(self.points) >= 2:
                self.finish_wall_segment(context, settings)
                self.points = []
                self.preview_point = None
                self.wall_obj = None
            else:
                self.update_mesh(context, settings)

            return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}

    def _handle_rectangle(self, context, settings, snapped):
        if self.rect_state == 0:
            self.rect_start = snapped
            self.rect_state = 1
            return {'RUNNING_MODAL'}
        else:
            p1 = self.rect_start
            p3 = snapped
            p2 = Vector((p3.x, p1.y, p1.z))
            p4 = Vector((p1.x, p3.y, p1.z))
            self.points = [p1, p2, p3, p4, p1]
            self.preview_point = None
            self.finish_wall_segment(context, settings)
            self.points = []
            self.rect_state = 0
            self.wall_obj = None
            return {'RUNNING_MODAL'}

    def get_snapped_pos(self, context, event, settings):
        raw = get_mouse_3d_on_grid(context, event)
        raw.z = 0.0

        if settings.draw_type == 'RECTANGLE' and self.rect_state == 1:
            return raw

        if not self.points:
            return raw

        last = self.points[-1]
        self.is_close_loop = False

        if len(self.points) >= 3:
            first = self.points[0]
            if (raw - first).length < self.close_threshold:
                self.is_close_loop = True
                return first.copy()

        for pt in self.points[:-1]:
            if (raw - pt).length < self.close_threshold:
                return pt.copy()

        if len(self.points) >= 2 and settings.wall_snap_mode == 'NONE':
            for i in range(len(self.points) - 1):
                p1 = self.points[i]
                p2 = self.points[i + 1]
                seg_dir = (p2 - p1).normalized()
                if seg_dir.length < 0.001:
                    continue
                to_raw = raw - p1
                perp = abs(cross2d(to_raw, seg_dir))
                if perp < self.collinear_threshold:
                    proj = p1 + seg_dir * to_raw.dot(seg_dir)
                    return Vector((proj.x, proj.y, 0.0))

        mode = settings.wall_snap_mode
        if mode == 'NONE':
            return raw
        elif mode == 'GRID':
            return snap_mouse(last, raw, 'GRID', grid_size=settings.wall_grid_size)
        elif mode == 'ANGLE':
            return snap_mouse(last, raw, 'ANGLE', angle_step=settings.wall_snap_angle)
        elif mode == 'ORTHO':
            return snap_mouse(last, raw, 'ORTHO', angle_step=float(settings.wall_ortho_angle))
        return snap_mouse(last, raw, 'ORTHO')

    def update_preview(self, context, event, settings):
        self.preview_point = self.get_snapped_pos(context, event, settings)
        self.update_mesh(context, settings)

    def _get_wall_type_data(self, context):
        settings = context.scene.cabinet_tool_settings
        types = context.scene.cabinet_wall_types
        wt = None
        if settings.wall_type_index < len(types):
            wt = types[settings.wall_type_index]
        if wt and wt.has_layers and len(wt.layers) > 0:
            total = sum(l.thickness for l in wt.layers)
            return total, wt
        return settings.wall_thickness, None

    def _build_centerline(self, context, settings):
        """Build final centerline: points + preview + fillet + location_line + offset."""
        pts = list(self.points)
        if self.preview_point and len(self.points) > 0:
            pts.append(self.preview_point)
        if len(pts) < 2:
            return None

        total_thick, wt = self._get_wall_type_data(context)

        # 1) Fillet (on whole path)
        if settings.wall_radius and settings.wall_chain and len(pts) >= 3:
            pts = fillet_points(pts, settings.wall_radius_value)

        # 2) Location line offset (whole path, using total thickness)
        pts = apply_location_line_offset(pts, settings.wall_location_line, total_thick)

        # 3) User offset (whole path)
        pts = apply_offset(pts, settings.wall_offset, settings.wall_offset_flip, total_thick)

        return pts, total_thick, wt

    def update_mesh(self, context, settings):
        result = self._build_centerline(context, settings)
        if result is None:
            return
        centerline, total_thick, wt = result

        if settings.draw_type == 'RECTANGLE' and self.rect_state == 1 and self.rect_start and self.preview_point:
            p1 = self.rect_start
            p3 = self.preview_point
            p2 = Vector((p3.x, p1.y, p1.z))
            p4 = Vector((p1.x, p3.y, p1.z))
            centerline = [p1, p2, p3, p4, p1]
            # For preview, use total thickness directly
            verts, faces = build_wall_geometry(centerline, total_thick, settings.wall_height,
                                               settings.wall_bottom_offset, settings.wall_top_offset)
            self._ensure_preview_obj(context, verts, faces)
            return

        verts, faces = build_wall_geometry(
            centerline, total_thick, settings.wall_height,
            settings.wall_bottom_offset, settings.wall_top_offset
        )
        self._ensure_preview_obj(context, verts, faces)

    def _ensure_preview_obj(self, context, verts, faces):
        if self.wall_obj is None:
            mesh = bpy.data.meshes.new("Wall_Preview")
            self.wall_obj = bpy.data.objects.new("Wall_Preview", mesh)
            context.collection.objects.link(self.wall_obj)
        mesh = self.wall_obj.data
        mesh.clear_geometry()
        mesh.from_pydata(verts, [], faces)
        mesh.update()

    def finish_wall_segment(self, context, settings):
        if len(self.points) < 2 and settings.draw_type != 'RECTANGLE':
            return

        result = self._build_centerline(context, settings)
        if result is None:
            return
        centerline, total_thick, wt = result

        if settings.draw_type == 'RECTANGLE':
            # Already built in points
            centerline = list(self.points)

        if wt and wt.has_layers and len(wt.layers) > 0:
            if wt.split_layers_as_objects:
                self._build_split_layers(context, centerline, wt, settings)
            else:
                self._build_merged_layers(context, centerline, wt, settings)
        else:
            verts, faces = build_wall_geometry(
                centerline, total_thick, settings.wall_height,
                settings.wall_bottom_offset, settings.wall_top_offset
            )
            mesh = bpy.data.meshes.new("Wall")
            obj = bpy.data.objects.new("Wall", mesh)
            context.collection.objects.link(obj)
            mesh.from_pydata(verts, [], faces)
            mesh.update()
            if settings.wall_material:
                if len(mesh.materials) == 0:
                    mesh.materials.append(settings.wall_material)
                else:
                    mesh.materials[0] = settings.wall_material
            self.wall_objects.append(obj)

        if self.wall_obj:
            mesh = self.wall_obj.data
            bpy.data.objects.remove(self.wall_obj)
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
            self.wall_obj = None

    def _build_split_layers(self, context, centerline, wt, settings):
        """Each layer = separate mesh, shifted from shared centerline."""
        total = sum(l.thickness for l in wt.layers)
        if total < 0.001:
            return

        cum = 0.0
        for layer in wt.layers:
            offset = (cum + layer.thickness / 2.0) - total / 2.0
            layer_line = shift_polyline(centerline, offset)
            verts, faces = build_wall_geometry(
                layer_line, layer.thickness, settings.wall_height,
                settings.wall_bottom_offset, settings.wall_top_offset
            )
            mesh = bpy.data.meshes.new(f"Wall_{layer.function}")
            obj = bpy.data.objects.new(f"Wall_{layer.function}", mesh)
            context.collection.objects.link(obj)
            mesh.from_pydata(verts, [], faces)
            mesh.update()
            if layer.material:
                if len(mesh.materials) == 0:
                    mesh.materials.append(layer.material)
                else:
                    mesh.materials[0] = layer.material
            self.wall_objects.append(obj)
            cum += layer.thickness

    def _build_merged_layers(self, context, centerline, wt, settings):
        """Single mesh with total thickness. Materials assigned by face region later."""
        total = sum(l.thickness for l in wt.layers)
        verts, faces = build_wall_geometry(
            centerline, total, settings.wall_height,
            settings.wall_bottom_offset, settings.wall_top_offset
        )
        mesh = bpy.data.meshes.new("Wall_Merged")
        obj = bpy.data.objects.new("Wall_Merged", mesh)
        context.collection.objects.link(obj)
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        # Assign exterior material (first layer) to slot 0, interior (last) to slot 1
        if wt.layers:
            ext = wt.layers[0].material
            if ext:
                mesh.materials.append(ext)
            else:
                mesh.materials.append(None)
            if len(wt.layers) > 1:
                inter = wt.layers[-1].material
                if inter:
                    mesh.materials.append(inter)
                else:
                    mesh.materials.append(None)
                # Simple: exterior faces = slot 0, interior = slot 1
                # We can't easily distinguish without bmesh bisect, so assign all to 0 for now
                for f in mesh.polygons:
                    f.material_index = 0
        self.wall_objects.append(obj)

    def draw_callback(self, context):
        region = context.region
        rv3d = context.space_data.region_3d

        if len(self.points) >= 2:
            verts_3d = []
            for p in self.points:
                v2d = view3d_utils.location_3d_to_region_2d(region, rv3d, p)
                if v2d:
                    verts_3d.append((v2d.x, v2d.y))
            if len(verts_3d) >= 2:
                gpu.state.blend_set('ALPHA')
                gpu.state.line_width_set(2.0)
                shader = gpu.shader.from_builtin('UNIFORM_COLOR')
                batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": verts_3d})
                shader.uniform_float("color", (0.0, 0.8, 0.2, 0.9))
                batch.draw(shader)
                gpu.state.line_width_set(1.0)
                gpu.state.blend_set('NONE')

        if len(self.points) > 0 and self.preview_point:
            last = self.points[-1]
            last_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, last)
            curr_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, self.preview_point)

            if last_2d and curr_2d:
                gpu.state.blend_set('ALPHA')

                if self.is_close_loop:
                    draw_dashed_line_2d((last_2d.x, last_2d.y), (curr_2d.x, curr_2d.y),
                                        (1.0, 0.9, 0.0, 0.95), dash_len=6, gap_len=3)
                    font_id = 0
                    blf.position(font_id, curr_2d.x + 12, curr_2d.y + 12, 0)
                    blf.size(font_id, 14)
                    blf.color(font_id, 1.0, 0.9, 0.0, 1.0)
                    blf.draw(font_id, "CLOSE")
                else:
                    draw_dashed_line_2d((last_2d.x, last_2d.y), (curr_2d.x, curr_2d.y),
                                        (0.2, 0.5, 1.0, 0.9), dash_len=10, gap_len=5)

                if len(self.points) >= 2 and not self.is_close_loop:
                    for i in range(len(self.points) - 1):
                        p1 = self.points[i]
                        p2 = self.points[i + 1]
                        seg_dir = (p2 - p1).normalized()
                        if seg_dir.length < 0.001:
                            continue
                        to_preview = self.preview_point - p1
                        perp = abs(cross2d(to_preview, seg_dir))
                        if perp < self.collinear_threshold:
                            p1_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, p1)
                            p2_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, p2)
                            if p1_2d and p2_2d:
                                draw_dashed_line_2d((p1_2d.x, p1_2d.y), (p2_2d.x, p2_2d.y),
                                                    (1.0, 0.8, 0.2, 0.35), dash_len=3, gap_len=5)

                length = (self.preview_point - last).length
                angle = degrees(atan2(self.preview_point.y - last.y, self.preview_point.x - last.x))
                mid_x = (last_2d.x + curr_2d.x) / 2
                mid_y = (last_2d.y + curr_2d.y) / 2
                font_id = 0
                blf.position(font_id, mid_x + 10, mid_y + 10, 0)
                blf.size(font_id, 16)
                blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
                blf.draw(font_id, f"L: {length:.2f}m A: {angle:.1f}°")

                gpu.state.blend_set('NONE')

    def finish(self, context, keep_walls=False):
        if self.draw_handle:
            bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, 'WINDOW')
            self.draw_handle = None
        settings = context.scene.cabinet_tool_settings
        settings.is_drawing = False
        if self.wall_obj:
            mesh = self.wall_obj.data
            bpy.data.objects.remove(self.wall_obj)
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
            self.wall_obj = None
        if not keep_walls:
            for obj in self.wall_objects:
                if obj and obj.name in bpy.data.objects:
                    mesh = obj.data
                    bpy.data.objects.remove(obj)
                    if mesh.users == 0:
                        bpy.data.meshes.remove(mesh)
            self.wall_objects = []


classes = [CABINET_OT_draw_wall]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
