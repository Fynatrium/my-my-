import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from math import atan2, cos, sin, pi, radians, degrees, sqrt
from bpy_extras import view3d_utils
import blf


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
    return origin + direction * t


def snap_mouse(last, current, mode='ORTHO', angle_step=90.0, grid_size=0.1):
    delta = current - last
    delta.z = 0
    if mode == 'ORTHO':
        angle = atan2(delta.y, delta.x)
        step = radians(angle_step)
        snapped = round(angle / step) * step
        return last + Vector((cos(snapped), sin(snapped), 0)) * delta.length
    elif mode == 'ANGLE':
        angle = atan2(delta.y, delta.x)
        step = radians(angle_step)
        snapped = round(angle / step) * step
        return last + Vector((cos(snapped), sin(snapped), 0)) * delta.length
    elif mode == 'GRID':
        return Vector((
            round(current.x / grid_size) * grid_size,
            round(current.y / grid_size) * grid_size, 0.0
        ))
    return Vector((current.x, current.y, 0.0))


def apply_offset(points, offset, flip, thickness):
    if offset == 0 or len(points) < 2:
        return points
    result = []
    n = None
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        d = (p2 - p1).normalized()
        n = Vector((-d.y, d.x, 0))
        if flip:
            n = -n
        result.append(p1 + n * offset)
    if n is not None:
        result.append(points[-1] + n * offset)
    return result


def apply_location_line_offset(points, location_line, thickness):
    if not points or len(points) < 2:
        return points
    t2 = thickness / 2.0
    offsets = {
        'WALL_CENTER': 0.0, 'CORE_CENTER': 0.0,
        'FINISH_EXTERIOR': -t2, 'FINISH_INTERIOR': t2,
        'CORE_EXTERIOR': -t2, 'CORE_INTERIOR': t2,
    }
    offset = offsets.get(location_line, 0.0)
    if offset == 0:
        return points
    result = []
    n = None
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        d = (p2 - p1).normalized()
        n = Vector((-d.y, d.x, 0))
        result.append(p1 + n * offset)
    if n is not None:
        result.append(points[-1] + n * offset)
    return result


def fillet_points(points, radius):
    if radius <= 0 or len(points) < 3:
        return points
    result = [points[0]]
    for i in range(1, len(points) - 1):
        p_prev = points[i - 1]
        p_curr = points[i]
        p_next = points[i + 1]
        d1 = (p_curr - p_prev).normalized()
        d2 = (p_next - p_curr).normalized()
        angle = abs(atan2(cross2d(d1, d2), d1.dot(d2)))
        if angle < 0.01:
            result.append(p_curr)
            continue
        bisector = (d1 - d2).normalized()
        if bisector.length < 0.001:
            result.append(p_curr)
            continue
        dist = radius / sin(angle / 2)
        center = p_curr + bisector * dist
        t1 = center + (p_prev - center).normalized() * radius
        t2 = center + (p_next - center).normalized() * radius
        result.append(t1)
        result.append(t2)
    result.append(points[-1])
    return result


def shift_polyline(points, offset):
    """Shift entire polyline by offset along local normals."""
    if len(points) < 2 or abs(offset) < 1e-6:
        return points
    result = []
    for i in range(len(points)):
        if i == 0:
            d = (points[1] - points[0]).normalized()
        elif i == len(points) - 1:
            d = (points[-1] - points[-2]).normalized()
        else:
            d1 = (points[i] - points[i - 1]).normalized()
            d2 = (points[i + 1] - points[i]).normalized()
            d = (d1 + d2).normalized()
        n = Vector((-d.y, d.x, 0))
        result.append(points[i] + n * offset)
    return result


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


def register():
    pass


def unregister():
    pass
