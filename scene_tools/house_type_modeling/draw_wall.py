import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from math import atan2, cos, sin, pi, radians, degrees
from bpy_extras import view3d_utils
import blf


# =============================================================================
# MATH HELPERS
# =============================================================================
def cross2d(a: Vector, b: Vector) -> float:
    return a.x * b.y - a.y * b.x


def get_mouse_3d_on_grid(context, event, z=0.0):
    region = context.region
    rv3d = context.space_data.region_3d
    coord = (event.mouse_region_x, event.mouse_region_y)
    origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    if abs(direction.z) < 1e-6:
        return view3d_utils.region_2d_to_location_3d(region, rv3d, coord, Vector((0, 0, z)))
    t = (z - origin.z) / direction.z
    hit = origin + direction * t
    return hit


def snap_mouse(last, current, mode='ORTHO', angle_step=90.0, grid_size=0.1):
    delta = current - last
    delta.z = 0
    if mode == 'ORTHO':
        angle = atan2(delta.y, delta.x)
        step = pi / 2
        snapped = round(angle / step) * step
        dist = delta.length
        return last + Vector((cos(snapped), sin(snapped), 0)) * dist
    elif mode == 'ANGLE':
        angle = atan2(delta.y, delta.x)
        step = radians(angle_step)
        snapped = round(angle / step) * step
        dist = delta.length
        return last + Vector((cos(snapped), sin(snapped), 0)) * dist
    elif mode == 'GRID':
        return Vector((
            round(current.x / grid_size) * grid_size,
            round(current.y / grid_size) * grid_size,
            0.0
        ))
    else:
        return Vector((current.x, current.y, 0.0))


def build_wall_geometry(points, thickness, height, bottom_offset=0.0, top_offset=0.0):
    n = len(points)
    if n < 2:
        return [], []
    t2 = thickness / 2.0
    dirs = []
    left_normals = []
    for i in range(n - 1):
        d = (points[i + 1] - points[i]).normalized()
        d.z = 0
        d.normalize()
        dirs.append(d)
        left_normals.append(Vector((-d.y, d.x, 0)))

    left_edge = []
    right_edge = []
    left_edge.append(points[0] + left_normals[0] * t2)
    right_edge.append(points[0] - left_normals[0] * t2)

    for i in range(1, n - 1):
        d1 = dirs[i - 1]
        d2 = dirs[i]
        n1 = left_normals[i - 1]
        n2 = left_normals[i]
        diff = (n2 - n1) * t2
        det = cross2d(d1, d2)
        if abs(det) < 1e-6:
            avg_n = (n1 + n2).normalized()
            left_edge.append(points[i] + avg_n * t2)
            right_edge.append(points[i] - avg_n * t2)
        else:
            s1 = cross2d(diff, d2) / det
            miter_left = points[i] + n1 * t2 + d1 * s1
            diff_r = (-n2 + n1) * t2
            s1_r = cross2d(diff_r, d2) / det
            miter_right = points[i] - n1 * t2 + d1 * s1_r
            left_edge.append(miter_left)
            right_edge.append(miter_right)

    left_edge.append(points[-1] + left_normals[-1] * t2)
    right_edge.append(points[-1] - left_normals[-1] * t2)

    verts = []
    z_bottom = bottom_offset
    z_top = height - top_offset

    for i in range(n):
        verts.append(left_edge[i] + Vector((0, 0, z_bottom)))
        verts.append(right_edge[i] + Vector((0, 0, z_bottom)))
    for i in range(n):
        verts.append(left_edge[i] + Vector((0, 0, z_top)))
        verts.append(right_edge[i] + Vector((0, 0, z_top)))

    faces = []
    for i in range(n - 1):
        lb0 = i * 2
        rb0 = i * 2 + 1
        lb1 = (i + 1) * 2
        rb1 = (i + 1) * 2 + 1
        lt0 = lb0 + n * 2
        rt0 = rb0 + n * 2
        lt1 = lb1 + n * 2
        rt1 = rb1 + n * 2
        faces.append((lb0, rb0, rb1, lb1))
        faces.append((lt0, lt1, rt1, rt0))
        faces.append((lb0, lb1, lt1, lt0))
        faces.append((rb0, rt0, rt1, rb1))

    if n >= 2:
        faces.append((0, 1, 1 + n * 2, 0 + n * 2))
        end_lb = (n - 1) * 2
        end_rb = end_lb + 1
        end_lt = end_lb + n * 2
        end_rt = end_rb + n * 2
        faces.append((end_lb, end_lt, end_rt, end_rb))

    return verts, faces


def draw_dashed_line_2d(start_2d, end_2d, color, dash_len=8, gap_len=4):
    if not start_2d or not end_2d:
        return
    dx = end_2d[0] - start_2d[0]
    dy = end_2d[1] - start_2d[1]
    total_len = (dx ** 2 + dy ** 2) ** 0.5
    if total_len < 1e-6:
        return
    nx = dx / total_len
    ny = dy / total_len
    pos = []
    cur_len = 0
    while cur_len < total_len:
        seg_start = cur_len
        seg_end = min(cur_len + dash_len, total_len)
        pos.append((start_2d[0] + nx * seg_start, start_2d[1] + ny * seg_start))
        pos.append((start_2d[0] + nx * seg_end, start_2d[1] + ny * seg_end))
        cur_len += dash_len + gap_len
    if len(pos) >= 2:
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'LINES', {"pos": pos})
        shader.uniform_float("color", color)
        batch.draw(shader)


# =============================================================================
# MODAL OPERATOR
# =============================================================================
class CABINET_OT_draw_wall(bpy.types.Operator):
    bl_idname = "cabinet.draw_wall"
    bl_label = "Draw Wall"
    bl_description = "Draw continuous wall like Revit"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.points = []
        self.preview_point = None
        self.wall_obj = None
        self.draw_handle = None
        self.collinear_threshold = 0.15
        self.close_threshold = 0.30
        self.is_close_loop = False

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def invoke(self, context, event):
        try:
            context.scene.cabinet_active_tool = 'DRAW_WALL'
        except AttributeError:
            pass
        mesh = bpy.data.meshes.new("Wall")
        self.wall_obj = bpy.data.objects.new("Wall", mesh)
        context.collection.objects.link(self.wall_obj)
        context.view_layer.objects.active = self.wall_obj
        args = (context,)
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, args, 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        settings = context.scene.cabinet_tool_settings

        if event.type == 'ESC':
            self.finish(context, cancelled=True)
            return {'CANCELLED'}

        if event.type == 'RET' and event.value == 'PRESS':
            if len(self.points) >= 2:
                self.finish(context, cancelled=False)
                return {'FINISHED'}
            else:
                self.finish(context, cancelled=True)
                return {'CANCELLED'}

        if event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
            if len(self.points) > 1:
                self.points.pop()
                self.update_mesh(context, settings)
                return {'RUNNING_MODAL'}
            else:
                self.finish(context, cancelled=True)
                return {'CANCELLED'}

        if event.type == 'MOUSEMOVE':
            self.update_preview(context, event, settings)
            return {'PASS_THROUGH'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            snapped = self.get_snapped_pos(context, event, settings)

            if not self.points:
                self.points.append(snapped)
                return {'RUNNING_MODAL'}

            # Close loop detection
            if len(self.points) >= 3 and self.is_close_loop:
                self.points.append(self.points[0].copy())
                self.finish(context, cancelled=False)
                return {'FINISHED'}

            self.points.append(snapped)
            self.update_mesh(context, settings)
            return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}

    def get_snapped_pos(self, context, event, settings):
        raw = get_mouse_3d_on_grid(context, event)
        raw.z = 0.0

        if not self.points:
            return raw

        last = self.points[-1]
        self.is_close_loop = False

        # --- Close Loop Snap ---
        if len(self.points) >= 3:
            first = self.points[0]
            dist_to_first = (raw - first).length
            if dist_to_first < self.close_threshold:
                self.is_close_loop = True
                return first.copy()

        # --- Collinear Snap (Revit extension line) ---
        if len(self.points) >= 2 and settings.wall_snap_mode == 'NONE':
            for i in range(len(self.points) - 1):
                p1 = self.points[i]
                p2 = self.points[i + 1]
                seg_dir = (p2 - p1).normalized()
                if seg_dir.length < 0.001:
                    continue
                to_raw = raw - p1
                perp_dist = abs(cross2d(to_raw, seg_dir))
                if perp_dist < self.collinear_threshold:
                    proj_dist = to_raw.dot(seg_dir)
                    proj = p1 + seg_dir * proj_dist
                    return Vector((proj.x, proj.y, 0.0))

        # --- Standard Snap Modes ---
        mode = settings.wall_snap_mode
        if mode == 'NONE':
            return raw
        elif mode == 'GRID':
            return snap_mouse(last, raw, 'GRID', grid_size=settings.wall_grid_size)
        elif mode == 'ANGLE':
            return snap_mouse(last, raw, 'ANGLE', angle_step=settings.wall_snap_angle)
        else:
            return snap_mouse(last, raw, 'ORTHO')

    def update_preview(self, context, event, settings):
        self.preview_point = self.get_snapped_pos(context, event, settings)
        self.update_mesh(context, settings)

    def update_mesh(self, context, settings):
        pts = list(self.points)
        if self.preview_point and len(self.points) > 0:
            pts.append(self.preview_point)
        if len(pts) < 2:
            return

        verts, faces = build_wall_geometry(
            pts,
            settings.wall_thickness,
            settings.wall_height,
            settings.wall_bottom_offset,
            settings.wall_top_offset
        )
        mesh = self.wall_obj.data
        mesh.clear_geometry()
        mesh.from_pydata(verts, [], faces)
        mesh.update()

    def draw_callback(self, context):
        region = context.region
        rv3d = context.space_data.region_3d

        # --- Draw existing confirmed segments (solid green) ---
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

        # --- Draw preview segment ---
        if len(self.points) > 0 and self.preview_point:
            last = self.points[-1]
            last_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, last)
            curr_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, self.preview_point)

            if last_2d and curr_2d:
                gpu.state.blend_set('ALPHA')

                # Color: yellow if close loop, blue otherwise
                if self.is_close_loop:
                    draw_dashed_line_2d(
                        (last_2d.x, last_2d.y),
                        (curr_2d.x, curr_2d.y),
                        (1.0, 0.9, 0.0, 0.95),
                        dash_len=6, gap_len=3
                    )
                    # Draw "CLOSE" text
                    font_id = 0
                    blf.position(font_id, curr_2d.x + 12, curr_2d.y + 12, 0)
                    blf.size(font_id, 14)
                    blf.color(font_id, 1.0, 0.9, 0.0, 1.0)
                    blf.draw(font_id, "CLOSE")
                else:
                    draw_dashed_line_2d(
                        (last_2d.x, last_2d.y),
                        (curr_2d.x, curr_2d.y),
                        (0.2, 0.5, 1.0, 0.9),
                        dash_len=10, gap_len=5
                    )

                # --- Collinear extension indicator ---
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
                                draw_dashed_line_2d(
                                    (p1_2d.x, p1_2d.y),
                                    (p2_2d.x, p2_2d.y),
                                    (1.0, 0.8, 0.2, 0.35),
                                    dash_len=3, gap_len=5
                                )

                # --- Dimension text ---
                length = (self.preview_point - last).length
                angle = degrees(atan2(
                    self.preview_point.y - last.y,
                    self.preview_point.x - last.x
                ))
                mid_x = (last_2d.x + curr_2d.x) / 2
                mid_y = (last_2d.y + curr_2d.y) / 2
                font_id = 0
                blf.position(font_id, mid_x + 10, mid_y + 10, 0)
                blf.size(font_id, 16)
                blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
                blf.draw(font_id, f"L: {length:.2f}m  A: {angle:.1f}\u00b0")

                gpu.state.blend_set('NONE')

    def finish(self, context, cancelled=False):
        if self.draw_handle:
            bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, 'WINDOW')
            self.draw_handle = None

        try:
            context.scene.cabinet_active_tool = 'NONE'
        except AttributeError:
            pass

        if cancelled:
            if self.wall_obj:
                mesh = self.wall_obj.data
                bpy.data.objects.remove(self.wall_obj)
                if mesh.users == 0:
                    bpy.data.meshes.remove(mesh)
                self.wall_obj = None
        else:
            if len(self.points) < 2:
                if self.wall_obj:
                    mesh = self.wall_obj.data
                    bpy.data.objects.remove(self.wall_obj)
                    if mesh.users == 0:
                        bpy.data.meshes.remove(mesh)
                    self.wall_obj = None
            else:
                settings = context.scene.cabinet_tool_settings
                # IMPORTANT: use only self.points, NOT preview_point
                verts, faces = build_wall_geometry(
                    self.points,
                    settings.wall_thickness,
                    settings.wall_height,
                    settings.wall_bottom_offset,
                    settings.wall_top_offset
                )
                mesh = self.wall_obj.data
                mesh.clear_geometry()
                mesh.from_pydata(verts, [], faces)
                mesh.update()

                if settings.wall_material:
                    if len(self.wall_obj.data.materials) == 0:
                        self.wall_obj.data.materials.append(settings.wall_material)
                    else:
                        self.wall_obj.data.materials[0] = settings.wall_material


classes = [
    CABINET_OT_draw_wall,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
