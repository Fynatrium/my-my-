import bpy
from bpy.types import Panel, Operator
from .layout_constants import (
    WALL_TYPE_LABEL_W, WALL_TYPE_WIDGET_SX, WALL_TYPE_WIDGET_SY, WALL_TYPE_ROW_SY,
    WALL_TYPE_PREVIEW_X, WALL_TYPE_PREVIEW_Y,
    split_prop
)


class CABINET_OT_edit_wall_type(Operator):
    bl_idname = "cabinet.edit_wall_type"
    bl_label = "Edit Type"
    bl_options = {'REGISTER'}

    def execute(self, context):
        self.report({'INFO'}, "Use the new Type Properties dialog.")
        return {'FINISHED'}


def draw_wall_type_popover(layout, context):
    settings = context.scene.cabinet_tool_settings
    scene = context.scene
    types = scene.cabinet_wall_types

    box = layout.box()

    # ── Preview + Dropdown merged ──
    row = box.row(align=True)
    row.scale_x = WALL_TYPE_PREVIEW_X
    row.scale_y = WALL_TYPE_PREVIEW_Y * 1.5

    thumb = row.column(align=True)
    thumb.scale_x = 0.8
    thumb.label(text="", icon='MESH_PLANE')

    info = row.column(align=True)
    info.scale_x = 1.5
    if len(types) > 0 and settings.wall_type_index < len(types):
        wt = types[settings.wall_type_index]
        info.label(text=wt.family)
        info.label(text=wt.name)
        if wt.has_layers and len(wt.layers) > 0:
            total = sum(l.thickness for l in wt.layers)
            info.label(text=f"{total:.3f} m (layered)")
        else:
            info.label(text=f"{wt.thickness:.3f} m")
    else:
        info.label(text="Basic Wall")
        info.label(text="Generic - 200mm")
        info.label(text="0.2 m")

    row2 = box.row(align=True)
    row2.scale_y = 1.2
    row2.prop(settings, "wall_type_enum", text="")

    # ── Split/Merged toggle (only for layered walls) ──
    if len(types) > 0 and settings.wall_type_index < len(types):
        wt = types[settings.wall_type_index]
        if wt.has_layers and len(wt.layers) > 0:
            row = box.row(align=True)
            row.prop(wt, "split_layers_as_objects", toggle=True,
                     text="Split Layers" if wt.split_layers_as_objects else "Merged Layers")

    # ── Edit Type button ──
    row3 = box.row(align=True)
    row3.scale_y = 1.1
    row3.operator("cabinet.wall_type_editor", text="Edit Type", icon='FULLSCREEN_ENTER')


class CABINET_PT_popover_wall_type(Panel):
    bl_label = "Wall Type"
    bl_idname = "CABINET_PT_popover_wall_type"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 24

    def draw(self, context):
        draw_wall_type_popover(self.layout, context)


classes = [
    CABINET_OT_edit_wall_type,
    CABINET_PT_popover_wall_type,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
