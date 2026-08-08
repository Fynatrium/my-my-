import bpy
from bpy.types import Operator, UIList
from bpy.props import EnumProperty


def _get_active_wall_type(context):
    scene = context.scene
    settings = scene.cabinet_tool_settings
    idx = settings.wall_type_index
    types = scene.cabinet_wall_types
    if 0 <= idx < len(types):
        return types[idx], idx
    return None, -1


# ═══════════════════════════════════════════════════════════════════════
# UIList: Layers
# ═══════════════════════════════════════════════════════════════════════

class CABINET_UL_wall_layers(UIList):
    bl_idname = "CABINET_UL_wall_layers"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            icon_map = {
                'STRUCTURE': 'MOD_SOLIDIFY',
                'SUBSTRATE': 'TEXTURE',
                'THERMAL': 'FREEZE',
                'FINISH1': 'COLOR',
                'FINISH2': 'MATERIAL',
                'MEMBRANE': 'MOD_CLOTH',
            }
            row.label(text=item.function, icon=icon_map.get(item.function, 'BLANK1'))
            row.label(text=f"{item.thickness:.3f} m")
            mat_name = item.material.name if item.material else "—"
            row.label(text=mat_name)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text=item.function)


# ═══════════════════════════════════════════════════════════════════════
# Layer Operators
# ═══════════════════════════════════════════════════════════════════════

class CABINET_OT_layer_add(Operator):
    bl_idname = "cabinet.layer_add"
    bl_label = "Add Layer"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(
        name="Direction",
        items=[('ABOVE', "Above", ""), ('BELOW', "Below", "")],
        default='BELOW'
    )

    def execute(self, context):
        wt, idx = _get_active_wall_type(context)
        if wt is None:
            return {'CANCELLED'}

        active = wt.active_layer_index
        insert_at = active + 1 if self.direction == 'BELOW' else active
        if insert_at < 0:
            insert_at = 0
        if insert_at > len(wt.layers):
            insert_at = len(wt.layers)

        wt.layers.add()
        for i in range(len(wt.layers) - 1, insert_at, -1):
            wt.layers.move(i - 1, i)

        wt.active_layer_index = insert_at
        wt.has_layers = True
        return {'FINISHED'}


class CABINET_OT_layer_remove(Operator):
    bl_idname = "cabinet.layer_remove"
    bl_label = "Delete Layer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        wt, idx = _get_active_wall_type(context)
        if wt is None or wt.active_layer_index < 0:
            return {'CANCELLED'}
        wt.layers.remove(wt.active_layer_index)
        if wt.active_layer_index >= len(wt.layers):
            wt.active_layer_index = max(0, len(wt.layers) - 1)
        if len(wt.layers) == 0:
            wt.has_layers = False
        return {'FINISHED'}


class CABINET_OT_layer_move(Operator):
    bl_idname = "cabinet.layer_move"
    bl_label = "Move Layer"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(
        name="Direction",
        items=[('UP', "Up", ""), ('DOWN', "Down", "")],
        default='UP'
    )

    def execute(self, context):
        wt, idx = _get_active_wall_type(context)
        if wt is None:
            return {'CANCELLED'}
        active = wt.active_layer_index
        if self.direction == 'UP' and active > 0:
            wt.layers.move(active, active - 1)
            wt.active_layer_index -= 1
        elif self.direction == 'DOWN' and active < len(wt.layers) - 1:
            wt.layers.move(active, active + 1)
            wt.active_layer_index += 1
        return {'FINISHED'}


# ═══════════════════════════════════════════════════════════════════════
# Edit Assembly Dialog (modal)
# ═══════════════════════════════════════════════════════════════════════

class CABINET_OT_wall_type_assembly(Operator):
    bl_idname = "cabinet.wall_type_assembly"
    bl_label = "Edit Assembly"
    bl_description = "Edit wall layer composition"
    bl_options = {'REGISTER'}

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        wt, idx = _get_active_wall_type(context)

        if wt is None:
            layout.label(text="No wall type selected.", icon='ERROR')
            return

        layout.label(text=f"Assembly:  {wt.name}", icon='MOD_SOLIDIFY')
        layout.separator()

        # ── Layers table + controls ──
        split = layout.split(factor=0.55)

        # Left: list + buttons
        col = split.column(align=True)
        col.template_list(
            "CABINET_UL_wall_layers",
            "",
            wt, "layers",
            wt, "active_layer_index",
            rows=7,
        )

        sub = col.column(align=True)
        sub.scale_y = 0.9
        row = sub.row(align=True)
        row.operator("cabinet.layer_add", text="Insert Above", icon='ADD').direction = 'ABOVE'
        row = sub.row(align=True)
        row.operator("cabinet.layer_add", text="Insert Below", icon='ADD').direction = 'BELOW'
        row = sub.row(align=True)
        row.operator("cabinet.layer_remove", text="Delete", icon='REMOVE')
        sub.separator()
        row = sub.row(align=True)
        row.operator("cabinet.layer_move", text="Move Up", icon='TRIA_UP').direction = 'UP'
        row = sub.row(align=True)
        row.operator("cabinet.layer_move", text="Move Down", icon='TRIA_DOWN').direction = 'DOWN'

        # Right: layer properties + preview
        col = split.column(align=True)

        # Layer props
        if 0 <= wt.active_layer_index < len(wt.layers):
            layer = wt.layers[wt.active_layer_index]
            box = col.box()
            box.label(text="Layer Properties", icon='PROPERTIES')
            box.prop(layer, "function")
            box.prop(layer, "material", text="Material")
            box.prop(layer, "thickness")
            box.prop(layer, "wraps")
        else:
            col.label(text="Select a layer", icon='INFO')
            col.label(text="to edit properties.")

        col.separator()

        # ── 2D Section Preview with core boundaries ──
        preview = col.box()
        preview.label(text="Section Preview", icon='VIEW3D')

        if wt.has_layers and len(wt.layers) > 0:
            # Build preview rows with boundary lines
            pcol = preview.column(align=True)

            # Determine core range (STRUCTURE layers = core)
            core_start = -1
            core_end = -1
            for i, layer in enumerate(wt.layers):
                if layer.function == 'STRUCTURE':
                    if core_start == -1:
                        core_start = i
                    core_end = i

            for i, layer in enumerate(wt.layers):
                lr = pcol.row(align=True)
                lr.scale_y = max(1.2, layer.thickness * 20)

                # Color by function
                colors = {
                    'STRUCTURE': (0.45, 0.45, 0.45, 1.0),
                    'SUBSTRATE': (0.55, 0.40, 0.30, 1.0),
                    'THERMAL': (0.20, 0.50, 0.70, 1.0),
                    'FINISH1': (0.80, 0.75, 0.65, 1.0),
                    'FINISH2': (0.75, 0.70, 0.60, 1.0),
                    'MEMBRANE': (0.90, 0.30, 0.30, 1.0),
                }
                c = colors.get(layer.function, (0.5, 0.5, 0.5, 1.0))

                # Core boundary indicator
                is_core_boundary = (i == core_start and core_start != -1) or (i == core_end + 1 and core_end != -1)
                boundary_icon = 'TRIA_RIGHT' if is_core_boundary else 'BLANK1'
                boundary_text = "│" if is_core_boundary else "  "

                lr.label(text=boundary_text, icon=boundary_icon)
                lr.label(text=f"  {layer.function}")
                lr.label(text=f"{layer.thickness:.3f} m")

            # Core labels
            if core_start != -1:
                row = preview.row()
                row.alignment = 'CENTER'
                row.label(text="◄── Core Boundary ──►", icon='ARROW_LEFTRIGHT')
        else:
            row = preview.row(align=True)
            row.scale_y = 3.0
            row.label(text="  Basic Wall", icon='MOD_SOLIDIFY')
            row.label(text=f"{wt.thickness:.3f} m")

        layout.separator()

        # ── Total thickness ──
        total = sum(l.thickness for l in wt.layers)
        row = layout.row(align=True)
        row.scale_y = 1.3
        row.alert = True
        row.label(text="Total Thickness:")
        row.label(text=f"{total:.3f} m")

        # ── Convert to basic / layered toggle ──
        layout.separator()
        row = layout.row(align=True)
        if wt.has_layers:
            row.label(text="Mode:  Layered Wall")
            row.operator("cabinet.wall_type_clear_layers", text="Reset to Basic", icon='LOOP_BACK')
        else:
            row.label(text="Mode:  Basic Wall")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=760)


class CABINET_OT_wall_type_clear_layers(Operator):
    bl_idname = "cabinet.wall_type_clear_layers"
    bl_label = "Reset to Basic"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        wt, idx = _get_active_wall_type(context)
        if wt is None:
            return {'CANCELLED'}
        wt.layers.clear()
        wt.has_layers = False
        wt.active_layer_index = -1
        return {'FINISHED'}


classes = [
    CABINET_UL_wall_layers,
    CABINET_OT_layer_add,
    CABINET_OT_layer_remove,
    CABINET_OT_layer_move,
    CABINET_OT_wall_type_assembly,
    CABINET_OT_wall_type_clear_layers,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
