import bpy
from bpy.types import Panel, Operator
from .layout_constants import (
    MODIFY_BTN_SX, MODIFY_BTN_SY, MODIFY_LABEL_W, MODIFY_WIDGET_SX, MODIFY_WIDGET_SY, MODIFY_ROW_SY,
    split_prop
)


class CABINET_OT_chin(Operator):
    bl_idname = "cabinet.chin"
    bl_label = "Chin"
    bl_options = {'REGISTER'}
    def execute(self, context):
        self.report({'INFO'}, "Chin clicked")
        return {'FINISHED'}


class CABINET_OT_radios(Operator):
    bl_idname = "cabinet.radios"
    bl_label = "Radios"
    bl_options = {'REGISTER'}
    def execute(self, context):
        self.report({'INFO'}, "Radios clicked")
        return {'FINISHED'}


class CABINET_OT_align(Operator):
    bl_idname = "cabinet.align"
    bl_label = "Align"
    bl_options = {'REGISTER'}
    def execute(self, context):
        self.report({'INFO'}, "Align clicked")
        return {'FINISHED'}


class CABINET_OT_offset(Operator):
    bl_idname = "cabinet.offset"
    bl_label = "Offset"
    bl_options = {'REGISTER'}
    def execute(self, context):
        self.report({'INFO'}, "Offset clicked")
        return {'FINISHED'}


class CABINET_OT_mirror(Operator):
    bl_idname = "cabinet.mirror"
    bl_label = "Mirror"
    bl_options = {'REGISTER'}
    def execute(self, context):
        self.report({'INFO'}, "Mirror clicked")
        return {'FINISHED'}


def draw_modify_popover(layout, context):
    settings = context.scene.cabinet_tool_settings

    col = layout.column(align=True)

    # ── Geometry ──
    col.label(text="Geometry")
    split_prop(col, settings, "join_status", "Join Status",
               MODIFY_LABEL_W, MODIFY_WIDGET_SX, MODIFY_WIDGET_SY, MODIFY_ROW_SY)

    col.separator()

    # ── Edit ──
    col.label(text="Edit")
    row = col.row(align=True)
    row.scale_x = MODIFY_BTN_SX
    row.scale_y = MODIFY_BTN_SY
    row.operator("mesh.split", text="Split")
    row.operator("mesh.edge_slide", text="Slide")
    row.operator("mesh.bridge_edge_loops", text="Join")

    col.separator()

    # ── Snap ──
    col.label(text="Snap")
    row = col.row(align=True)
    row.prop(settings, "wall_snap_mode", expand=True)

    if settings.wall_snap_mode == 'ORTHO':
        row = col.row(align=True)
        row.prop(settings, "wall_ortho_angle", expand=True)
    elif settings.wall_snap_mode == 'ANGLE':
        row = col.row(align=True)
        row.prop(settings, "wall_snap_angle", slider=True)
    elif settings.wall_snap_mode == 'GRID':
        row = col.row(align=True)
        row.prop(settings, "wall_grid_size")

    col.separator()

    # ── Location Line (dropdown) ──
    col.label(text="Location Line:")
    col.prop(settings, "wall_location_line", text="")

    col.separator()

    # ── Offset / Chain ──
    row = col.row(align=True)
    row.prop(settings, "wall_chain", toggle=True)
    row.prop(settings, "wall_even_thickness", toggle=True)

    row = col.row(align=True)
    row.prop(settings, "wall_offset")
    row.prop(settings, "wall_offset_flip", toggle=True, text="Flip")

    # ── Radius (fillet) ──
    row = col.row(align=True)
    row.prop(settings, "wall_radius", toggle=True)
    if settings.wall_radius:
        row.prop(settings, "wall_radius_value", text="Radius")


class CABINET_PT_popover_modify(Panel):
    bl_label = "Modify"
    bl_idname = "CABINET_PT_popover_modify"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 22

    def draw(self, context):
        draw_modify_popover(self.layout, context)


classes = [
    CABINET_OT_chin,
    CABINET_OT_radios,
    CABINET_OT_align,
    CABINET_OT_offset,
    CABINET_OT_mirror,
    CABINET_PT_popover_modify,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
