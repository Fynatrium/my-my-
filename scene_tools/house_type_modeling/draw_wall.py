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


def snap_mouse(last: Vector, current: Vector, mode: str, angle_step: float = 90.0, grid_size: float = 0.1) -> Vector:
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
        return Vector((round(current.x / grid_size) * grid_size, round(current.y / grid_size) * grid_size, 0.0))
    else:
        return Vector((current.x, current.y, 0.0))


def build_wall_geometry(points, thickness, height):
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
    for i in range(n):
        verts.append(left_edge[i])
        verts.append(right_edge[i])
    for i in range(n):
        verts.append(left_edge[i] + Vector((0, 0, height)))
        verts.append(right_edge[i] + Vector((0, 0, height)))
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


# =============================================================================
# MODAL OPERATOR
# =============================================================================
class CABINET_OT_draw_wall(bpy.types.Operator):
    bl_idname = "cabinet.draw_wall"
    bl_label = "Draw Wall"
    bl_description = "Draw continuous wall like Revit"
    bl_options = {'REGISTER', 'UNDO', 'GRAB_CURSOR', 'BLOCKING'}
    
    def __init__(self):
        self.points = []
        self.preview_point = None
        self.wall_obj = None
        self.draw_handle = None
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'
    
    def invoke(self, context, event):
        # Safe set active tool (works even if tool_options.py not loaded)
        try:
            context.scene.cabinet_active_tool = 'DRAW_WALL'
        except AttributeError:
            pass
        mesh = bpy.data.meshes.new("Wall")
        self.wall_obj = bpy.data.objects.new("Wall", mesh)
        context.collection.objects.link(self.wall_obj)
        context.view_layer.objects.active = self.wall_obj
        args = (context,)
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, args, 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        settings = context.scene.cabinet_tool_settings
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            self.finish(context, cancelled=True)
            return {'CANCELLED'}
        if event.type == 'RET' and event.value == 'PRESS':
            self.finish(context, cancelled=False)
            return {'FINISHED'}
        if event.type == 'MOUSEMOVE':
            self.update_preview(context, event, settings)
            return {'RUNNING_MODAL'}
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            snapped = self.get_snapped_pos(context, event, settings)
            if not self.points:
                self.points.append(snapped)
            else:
                self.points.append(snapped)
            self.update_mesh(context, settings)
            return {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}
    
    def get_snapped_pos(self, context, event, settings):
        raw = get_mouse_3d_on_grid(context, event)
        if not self.points:
            return Vector((raw.x, raw.y, 0.0))
        last = self.points[-1]
        mode = settings.wall_snap_mode
        if mode == 'NONE':
            return Vector((raw.x, raw.y, 0.0))
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
        verts, faces = build_wall_geometry(pts, settings.wall_thickness, settings.wall_height)
        mesh = self.wall_obj.data
        mesh.clear_geometry()
        mesh.from_pydata(verts, [], faces)
        mesh.update()
    
    def draw_callback(self, context):
        if len(self.points) == 0 or self.preview_point is None:
            return
        region = context.region
        rv3d = context.space_data.region_3d
        gpu.state.blend_set('ALPHA')
        gpu.state.line_width_set(2.0)
        if len(self.points) >= 2:
            verts_3d = []
            for p in self.points:
                v2d = view3d_utils.location_3d_to_region_2d(region, rv3d, p)
                if v2d:
                    verts_3d.append((v2d.x, v2d.y))
            if len(verts_3d) >= 2:
                shader = gpu.shader.from_builtin('UNIFORM_COLOR')
                batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": verts_3d})
                shader.uniform_float("color", (0.0, 0.8, 0.2, 0.8))
                batch.draw(shader)
        last = self.points[-1]
        last_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, last)
        curr_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, self.preview_point)
        if last_2d and curr_2d:
            shader = gpu.shader.from_builtin('UNIFORM_COLOR')
            batch = batch_for_shader(shader, 'LINES', {"pos": [(last_2d.x, last_2d.y), (curr_2d.x, curr_2d.y)]})
            shader.uniform_float("color", (0.2, 0.5, 1.0, 0.9))
            batch.draw(shader)
            length = (self.preview_point - last).length
            angle = degrees(atan2(self.preview_point.y - last.y, self.preview_point.x - last.x))
            mid_x = (last_2d.x + curr_2d.x) / 2
            mid_y = (last_2d.y + curr_2d.y) / 2
            font_id = 0
            blf.position(font_id, mid_x + 10, mid_y + 10, 0)
            blf.size(font_id, 16)
            blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
            blf.draw(font_id, f"L: {length:.2f}m  A: {angle:.1f}°")
        gpu.state.line_width_set(1.0)
        gpu.state.blend_set('NONE')
    
    def finish(self, context, cancelled=False):
        if self.draw_handle:
            bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, 'WINDOW')
            self.draw_handle = None
        try:
            context.scene.cabinet_active_tool = 'NONE'
        except AttributeError:
            pass
        if cancelled and self.wall_obj and len(self.points) < 2:
            mesh = self.wall_obj.data
            bpy.data.objects.remove(self.wall_obj)
            bpy.data.meshes.remove(mesh)


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