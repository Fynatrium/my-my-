bl_info = {
    "name": "Draw Wall",
    "author": "Cabinet Maker Pro",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Tool Header",
    "description": "Draw architectural walls with Revit-like workflow",
    "category": "3D View",
}

import bpy
from bpy.types import Operator, WorkSpaceTool
from bpy.props import StringProperty

from . import (
    properties,
    utils,
    draw_wall_operator,
    wall_type,
    wall_type_editor,
    wall_type_assembly,
    constraints,
    cross_section,
    structural,
    dimensions,
    modify,
    draw_type,
)


# ═══════════════════════════════════════════════════════════════════════
# Operators
# ═══════════════════════════════════════════════════════════════════════

class CABINET_OT_activate_draw_wall(Operator):
    bl_idname = "cabinet.activate_draw_wall"
    bl_label = "Draw Wall"
    bl_description = "Activate Draw Wall tool"
    bl_options = {'REGISTER'}

    def execute(self, context):
        is_active = getattr(context.scene, 'cabinet_active_tool', '') == 'DRAW_WALL'
        if is_active:
            context.scene.cabinet_active_tool = 'NONE'
            try:
                bpy.ops.wm.tool_set_by_id(name="builtin.select_box")
            except RuntimeError:
                pass
        else:
            context.scene.cabinet_active_tool = 'DRAW_WALL'
            try:
                bpy.ops.wm.tool_set_by_id(name="cabinet.draw_wall_tool")
            except RuntimeError:
                pass
        _redraw_all()
        return {'FINISHED'}


class CABINET_OT_wall_draw_toggle(Operator):
    bl_idname = "cabinet.wall_draw_toggle"
    bl_label = "Start"
    bl_description = "Start or stop drawing walls"
    bl_options = {'REGISTER'}

    def execute(self, context):
        settings = context.scene.cabinet_tool_settings
        if settings.is_drawing:
            settings.is_drawing = False
        else:
            try:
                bpy.ops.cabinet.draw_wall('INVOKE_DEFAULT')
            except RuntimeError as e:
                self.report({'ERROR'}, str(e))
        _redraw_all()
        return {'FINISHED'}


def _redraw_all():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
                for region in area.regions:
                    if region.type in ('UI', 'TOOLS', 'TOOL_HEADER', 'WINDOW', 'HEADER'):
                        region.tag_redraw()


# ═══════════════════════════════════════════════════════════════════════
# Tool Header
# ═══════════════════════════════════════════════════════════════════════

def draw_cabinet_tool_header(self, context):
    if getattr(context.scene, 'cabinet_active_tool', '') != 'DRAW_WALL':
        return

    layout = self.layout
    row = layout.row(align=True)

    is_drawing = context.scene.cabinet_tool_settings.is_drawing
    btn = row.row(align=True)
    btn.alert = is_drawing
    if is_drawing:
        btn.operator("cabinet.wall_draw_toggle", text="Esc", icon='PAUSE', depress=True)
    else:
        btn.operator("cabinet.wall_draw_toggle", text="Start", icon='PLAY')

    row.separator(factor=0.8)

    row.popover("CABINET_PT_popover_wall_type", text="Wall Type")
    row.popover("CABINET_PT_popover_constraints", text="Constraints")
    row.popover("CABINET_PT_popover_cross_section", text="Cross-Section")
    row.popover("CABINET_PT_popover_structural", text="Structural")
    row.popover("CABINET_PT_popover_dimensions", text="Dimensions")
    row.popover("CABINET_PT_popover_modify", text="Modify")

    # Draw Type popover with active-mode icon
    settings = context.scene.cabinet_tool_settings
    icon_map = {
        'LINE': 'IPO_LINEAR',
        'RECTANGLE': 'MESH_PLANE',
        'CIRCLE': 'MESH_CIRCLE',
        'POLYGON': 'MESH_GRID',
        'PICK_LINE': 'CURVE_PATH',
    }
    active_icon = icon_map.get(settings.draw_type, 'IPO_LINEAR')
    row.popover("CABINET_PT_popover_draw_type", text="", icon=active_icon)


# ═══════════════════════════════════════════════════════════════════════
# Workspace Tool
# ═══════════════════════════════════════════════════════════════════════

class MESH_WT_draw_wall(WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'
    bl_idname = "cabinet.draw_wall_tool"
    bl_label = "Draw Wall"
    bl_description = "Draw architectural walls"
    bl_icon = "ops.mesh.extrude_region_move"
    bl_widget = None
    bl_keymap = (
        ("view3d.select", {"type": 'LEFTMOUSE', "value": 'PRESS'}, None),
    )

    def draw_settings(context, layout, tool):
        pass


# ═══════════════════════════════════════════════════════════════════════
# Register / Unregister
# ═══════════════════════════════════════════════════════════════════════

local_classes = [
    CABINET_OT_activate_draw_wall,
    CABINET_OT_wall_draw_toggle,
]


def register():
    # Sub-modules
    properties.register()
    utils.register()
    draw_wall_operator.register()
    wall_type.register()
    wall_type_editor.register()
    wall_type_assembly.register()
    constraints.register()
    cross_section.register()
    structural.register()
    dimensions.register()
    modify.register()
    draw_type.register()

    # Local classes
    for cls in local_classes:
        bpy.utils.register_class(cls)

    # Workspace tool
    bpy.utils.register_tool(MESH_WT_draw_wall, after={"builtin.select_box"}, separator=True)

    # Tool header
    bpy.types.VIEW3D_HT_tool_header.append(draw_cabinet_tool_header)


def unregister():
    # Tool header
    if draw_cabinet_tool_header in bpy.types.VIEW3D_HT_tool_header:
        bpy.types.VIEW3D_HT_tool_header.remove(draw_cabinet_tool_header)

    # Workspace tool
    try:
        bpy.utils.unregister_tool(MESH_WT_draw_wall)
    except:
        pass

    # Local classes
    for cls in reversed(local_classes):
        bpy.utils.unregister_class(cls)

    # Sub-modules (reverse order)
    draw_type.unregister()
    modify.unregister()
    dimensions.unregister()
    structural.unregister()
    cross_section.unregister()
    constraints.unregister()
    wall_type_assembly.unregister()
    wall_type_editor.unregister()
    wall_type.unregister()
    draw_wall_operator.unregister()
    utils.unregister()
    properties.unregister()


if __name__ == "__main__":
    register()
