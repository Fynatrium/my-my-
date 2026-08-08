import bpy
from bpy.types import Panel
from .layout_constants import (
    STRUCT_LABEL_W, STRUCT_WIDGET_SX, STRUCT_WIDGET_SY, STRUCT_ROW_SY,
    split_prop
)


def draw_structural_popover(layout, context):
    settings = context.scene.cabinet_tool_settings
    col = layout.column(align=True)
    col.label(text="Structural")
    split_prop(layout, settings, "wall_structural", "Structural",
               STRUCT_LABEL_W, STRUCT_WIDGET_SX, STRUCT_WIDGET_SY, STRUCT_ROW_SY)
    split_prop(layout, settings, "structural_usage", "Structural Usage",
               STRUCT_LABEL_W, STRUCT_WIDGET_SX, STRUCT_WIDGET_SY, STRUCT_ROW_SY)
    split_prop(layout, settings, "rebar_cover_exterior", "Rebar Cover - Exterior",
               STRUCT_LABEL_W, STRUCT_WIDGET_SX, STRUCT_WIDGET_SY, STRUCT_ROW_SY)
    split_prop(layout, settings, "rebar_cover_interior", "Rebar Cover - Interior",
               STRUCT_LABEL_W, STRUCT_WIDGET_SX, STRUCT_WIDGET_SY, STRUCT_ROW_SY)
    split_prop(layout, settings, "rebar_cover_other", "Rebar Cover - Other",
               STRUCT_LABEL_W, STRUCT_WIDGET_SX, STRUCT_WIDGET_SY, STRUCT_ROW_SY)


class CABINET_PT_popover_structural(Panel):
    bl_label = "Structural"
    bl_idname = "CABINET_PT_popover_structural"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 24

    def draw(self, context):
        draw_structural_popover(self.layout, context)


classes = [CABINET_PT_popover_structural]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
