import bpy
from bpy.types import Panel
from .layout_constants import (
    CROSS_LABEL_W, CROSS_WIDGET_SX, CROSS_WIDGET_SY, CROSS_ROW_SY,
    split_prop
)


def draw_cross_section_popover(layout, context):
    settings = context.scene.cabinet_tool_settings
    col = layout.column(align=True)
    col.label(text="Cross-Section Definition")
    split_prop(layout, settings, "cross_section", "Cross-Section",
               CROSS_LABEL_W, CROSS_WIDGET_SX, CROSS_WIDGET_SY, CROSS_ROW_SY)


class CABINET_PT_popover_cross_section(Panel):
    bl_label = "Cross-Section"
    bl_idname = "CABINET_PT_popover_cross_section"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 20

    def draw(self, context):
        draw_cross_section_popover(self.layout, context)


classes = [CABINET_PT_popover_cross_section]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
