import bpy
from bpy.types import Panel
from .layout_constants import (
    CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY,
    split_prop
)


def draw_constraints_popover(layout, context):
    settings = context.scene.cabinet_tool_settings

    split_prop(layout, settings, "wall_location_line", "Location Line",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)

    layout.separator()

    # Base Constraint (dropdown enum)
    split_prop(layout, settings, "wall_base_level_enum", "Base Constraint",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)
    split_prop(layout, settings, "wall_bottom_offset", "Base Offset",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)
    split_prop(layout, settings, "base_is_attached", "Base is Attached",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)
    split_prop(layout, settings, "base_extension", "Base Extension",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)

    layout.separator()

    # Top Constraint (dropdown enum)
    split_prop(layout, settings, "wall_top_level_enum", "Top Constraint",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)
    split_prop(layout, settings, "wall_unconnected_height", "Unconnected Height",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)
    split_prop(layout, settings, "wall_top_offset", "Top Offset",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)
    split_prop(layout, settings, "top_is_attached", "Top is Attached",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)
    split_prop(layout, settings, "top_extension", "Top Extension",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)

    layout.separator()
    split_prop(layout, settings, "room_bounding", "Room Bounding",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)
    split_prop(layout, settings, "related_to_mass", "Related to Mass",
               CONSTRAINTS_LABEL_W, CONSTRAINTS_WIDGET_SX, CONSTRAINTS_WIDGET_SY, CONSTRAINTS_ROW_SY)


class CABINET_PT_popover_constraints(Panel):
    bl_label = "Constraints"
    bl_idname = "CABINET_PT_popover_constraints"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 24

    def draw(self, context):
        draw_constraints_popover(self.layout, context)


classes = [CABINET_PT_popover_constraints]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
