import bpy
from bpy.types import Panel, Operator
from .layout_constants import (
    DRAW_BTN_SX, DRAW_BTN_SY,
    split_prop
)


class CABINET_OT_set_draw_mode(Operator):
    bl_idname = "cabinet.set_draw_mode"
    bl_label = "Set Draw Mode"
    bl_options = {'REGISTER'}

    mode: bpy.props.StringProperty(default='LINE')

    def execute(self, context):
        context.scene.cabinet_tool_settings.draw_type = self.mode
        return {'FINISHED'}


def draw_draw_type_popover(layout, context):
    settings = context.scene.cabinet_tool_settings
    col = layout.column(align=True)
    col.label(text="Draw Type")
    col.separator()

    row = col.row(align=True)
    row.scale_x = DRAW_BTN_SX
    row.scale_y = DRAW_BTN_SY

    modes = [
        ('LINE', "Line", 'IPO_LINEAR'),
        ('RECTANGLE', "Rect", 'MESH_PLANE'),
        ('CIRCLE', "Circle", 'MESH_CIRCLE'),
        ('POLYGON', "Poly", 'MESH_GRID'),
        ('PICK_LINE', "Pick", 'CURVE_PATH'),
    ]

    for mode, label, icon in modes:
        is_active = settings.draw_type == mode
        row.operator(
            "cabinet.set_draw_mode",
            text=label,
            icon=icon,
            depress=is_active
        ).mode = mode


class CABINET_PT_popover_draw_type(Panel):
    bl_label = "Draw Type"
    bl_idname = "CABINET_PT_popover_draw_type"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 18

    def draw(self, context):
        draw_draw_type_popover(self.layout, context)


classes = [
    CABINET_OT_set_draw_mode,
    CABINET_PT_popover_draw_type,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
