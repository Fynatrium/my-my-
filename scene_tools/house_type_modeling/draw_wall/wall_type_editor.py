import bpy
from bpy.types import Operator, Panel
from bpy.props import StringProperty, IntProperty


def _get_active_wall_type(context):
    scene = context.scene
    settings = scene.cabinet_tool_settings
    idx = settings.wall_type_index
    types = scene.cabinet_wall_types
    if 0 <= idx < len(types):
        return types[idx], idx
    return None, -1


# ═══════════════════════════════════════════════════════════════════════
# Operators: Duplicate / Rename / New / Delete
# ═══════════════════════════════════════════════════════════════════════

class CABINET_OT_wall_type_duplicate(Operator):
    bl_idname = "cabinet.wall_type_duplicate"
    bl_label = "Duplicate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        wt, idx = _get_active_wall_type(context)
        if wt is None:
            self.report({'WARNING'}, "No wall type selected")
            return {'CANCELLED'}
        scene = context.scene
        new = scene.cabinet_wall_types.add()
        new.name = wt.name + " (2)"
        new.family = wt.family
        new.thickness = wt.thickness
        new.structure = wt.structure
        new.has_layers = wt.has_layers
        for layer in wt.layers:
            nl = new.layers.add()
            nl.function = layer.function
            nl.material = layer.material
            nl.thickness = layer.thickness
            nl.wraps = layer.wraps
        context.scene.cabinet_tool_settings.wall_type_index = len(scene.cabinet_wall_types) - 1
        return {'FINISHED'}


class CABINET_OT_wall_type_new(Operator):
    bl_idname = "cabinet.wall_type_new"
    bl_label = "New"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        new = scene.cabinet_wall_types.add()
        new.name = "Basic Wall - 200mm"
        new.family = "Basic Wall"
        new.thickness = 0.2
        new.has_layers = False
        context.scene.cabinet_tool_settings.wall_type_index = len(scene.cabinet_wall_types) - 1
        return {'FINISHED'}


class CABINET_OT_wall_type_delete(Operator):
    bl_idname = "cabinet.wall_type_delete"
    bl_label = "Delete"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        wt, idx = _get_active_wall_type(context)
        if wt is None:
            return {'CANCELLED'}
        scene = context.scene
        scene.cabinet_wall_types.remove(idx)
        settings = scene.cabinet_tool_settings
        if settings.wall_type_index >= len(scene.cabinet_wall_types):
            settings.wall_type_index = max(0, len(scene.cabinet_wall_types) - 1)
        return {'FINISHED'}


class CABINET_OT_wall_type_rename(Operator):
    bl_idname = "cabinet.wall_type_rename"
    bl_label = "Rename"
    bl_options = {'REGISTER'}

    new_name: StringProperty(name="Name", default="")

    def execute(self, context):
        wt, idx = _get_active_wall_type(context)
        if wt is None or not self.new_name.strip():
            return {'CANCELLED'}
        wt.name = self.new_name.strip()
        return {'FINISHED'}

    def invoke(self, context, event):
        wt, idx = _get_active_wall_type(context)
        if wt:
            self.new_name = wt.name
        return context.window_manager.invoke_props_dialog(self, width=300)


# ═══════════════════════════════════════════════════════════════════════
# Type Properties Dialog (modal)
# ═══════════════════════════════════════════════════════════════════════

class CABINET_OT_wall_type_editor(Operator):
    bl_idname = "cabinet.wall_type_editor"
    bl_label = "Type Properties"
    bl_options = {'REGISTER'}

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings = scene.cabinet_tool_settings
        types = scene.cabinet_wall_types

        if len(types) == 0:
            layout.label(text="No wall types defined.", icon='ERROR')
            layout.operator("cabinet.wall_type_new", text="New Type", icon='ADD')
            return

        wt, idx = _get_active_wall_type(context)
        if wt is None:
            layout.label(text="Invalid selection.", icon='ERROR')
            return

        # ── Header: selector + actions ──
        row = layout.row(align=True)
        row.scale_y = 1.3
        row.prop(settings, "wall_type_enum", text="")
        row.operator("cabinet.wall_type_new", text="", icon='ADD')
        row.operator("cabinet.wall_type_duplicate", text="", icon='DUPLICATE')
        row.operator("cabinet.wall_type_rename", text="", icon='GREASEPENCIL')
        row.operator("cabinet.wall_type_delete", text="", icon='TRASH')

        layout.separator()

        # ── Preview Section (2D cross-section with core boundaries) ──
        preview_box = layout.box()
        preview_box.label(text="Preview  |  Section", icon='VIEW3D')

        if wt.has_layers and len(wt.layers) > 0:
            col = preview_box.column(align=True)

            # Find core range
            core_start = -1
            core_end = -1
            for i, layer in enumerate(wt.layers):
                if layer.function == 'STRUCTURE':
                    if core_start == -1:
                        core_start = i
                    core_end = i

            for i, layer in enumerate(wt.layers):
                lr = col.row(align=True)
                lr.scale_y = max(1.0, layer.thickness * 15)

                icon_map = {
                    'STRUCTURE': 'MOD_SOLIDIFY',
                    'SUBSTRATE': 'TEXTURE',
                    'THERMAL': 'FREEZE',
                    'FINISH1': 'COLOR',
                    'FINISH2': 'MATERIAL',
                    'MEMBRANE': 'MOD_CLOTH',
                }
                icon = icon_map.get(layer.function, 'BLANK1')

                is_core_boundary = (i == core_start and core_start != -1) or (i == core_end + 1 and core_end != -1)
                boundary_text = "│" if is_core_boundary else "  "
                boundary_icon = 'TRIA_RIGHT' if is_core_boundary else 'BLANK1'

                lr.label(text=boundary_text, icon=boundary_icon)
                lr.label(text=f"  {layer.function}", icon=icon)
                lr.label(text=f"{layer.thickness:.3f} m")
                mat_name = layer.material.name if layer.material else "—"
                lr.label(text=mat_name)

            total = sum(l.thickness for l in wt.layers)
            row = preview_box.row()
            row.alignment = 'RIGHT'
            row.label(text=f"Total: {total:.3f} m", icon='ARROW_LEFTRIGHT')

            if core_start != -1:
                row = preview_box.row()
                row.alignment = 'CENTER'
                row.label(text="◄── Core Boundary ──►", icon='ARROW_LEFTRIGHT')
        else:
            row = preview_box.row(align=True)
            row.scale_y = 3.0
            row.label(text="  Basic Wall", icon='MOD_SOLIDIFY')
            row.label(text=f"{wt.thickness:.3f} m")

        layout.separator()

        # ── Properties ──
        col = layout.column(align=True)
        col.prop(wt, "family", text="Family")
        col.prop(wt, "structure", text="Structure")

        if wt.has_layers and len(wt.layers) > 0:
            total = sum(l.thickness for l in wt.layers)
            row = col.row(align=True)
            row.label(text="Thickness:")
            row.label(text=f"{total:.3f} m  (driven by layers)")
        else:
            col.prop(wt, "thickness", text="Thickness")

        col.prop(wt, "structure", text="Description")

        layout.separator()

        # ── Edit Assembly ──
        row = layout.row(align=True)
        row.scale_y = 1.2
        row.operator("cabinet.wall_type_assembly", text="Edit Assembly…", icon='FULLSCREEN_ENTER')

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=520)


classes = [
    CABINET_OT_wall_type_duplicate,
    CABINET_OT_wall_type_new,
    CABINET_OT_wall_type_delete,
    CABINET_OT_wall_type_rename,
    CABINET_OT_wall_type_editor,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
