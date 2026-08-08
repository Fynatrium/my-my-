import bpy
from bpy.types import Panel
from .layout_constants import (
    DIM_LABEL_W, DIM_WIDGET_SX, DIM_WIDGET_SY, DIM_ROW_SY,
    split_prop
)


def draw_dimensions_popover(layout, context):
    settings = context.scene.cabinet_tool_settings
    col = layout.column(align=True)
    col.label(text="Dimensions")
    split_prop(layout, settings, "wall_length", "Length",
               DIM_LABEL_W, DIM_WIDGET_SX, DIM_WIDGET_SY, DIM_ROW_SY)
    split_prop(layout, settings, "wall_area", "Area",
               DIM_LABEL_W, DIM_WIDGET_SX, DIM_WIDGET_SY, DIM_ROW_SY)
    split_prop(layout, settings, "wall_volume", "Volume",
               DIM_LABEL_W, DIM_WIDGET_SX, DIM_WIDGET_SY, DIM_ROW_SY)


class CABINET_PT_popover_dimensions(Panel):
    bl_label = "Dimensions"
    bl_idname = "CABINET_PT_popover_dimensions"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 20

    def draw(self, context):
        draw_dimensions_popover(self.layout, context)


classes = [CABINET_PT_popover_dimensions]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
