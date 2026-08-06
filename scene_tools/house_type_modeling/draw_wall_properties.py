import bpy
from bpy.props import (
    FloatProperty, EnumProperty, StringProperty,
    BoolProperty, PointerProperty
)


class CabinetToolSettings(bpy.types.PropertyGroup):
    # --- Drawing State ---
    is_drawing: BoolProperty(name="Is Drawing", default=False)

    # --- Snap Settings ---
    wall_snap_mode: EnumProperty(
        name="Snap",
        items=[
            ('NONE', "None", "Free movement"),
            ('ORTHO', "Ortho", "Snap to 90 degrees"),
            ('ANGLE', "Angle", "Snap to custom angle step"),
            ('GRID', "Grid", "Snap to grid"),
            ('FREE', "Free", "No snapping"),
        ],
        default='ORTHO'
    )
    wall_snap_angle: FloatProperty(
        name="Angle Step", default=90.0,
        min=1.0, max=180.0, step=5.0
    )
    wall_grid_size: FloatProperty(
        name="Grid Size", default=0.1,
        min=0.001, step=0.01, precision=3, unit='LENGTH'
    )
    wall_even_thickness: BoolProperty(
        name="Even Thickness",
        description="Maintain even wall thickness at corners",
        default=True
    )

    # --- Wall Type ---
    wall_type: EnumProperty(
        name="Wall Type",
        items=[
            ('BASIC', "Basic", "Basic wall", 'MESH_PLANE', 0),
            ('BRICK', "Brick", "Brick wall", 'MOD_BUILD', 1),
            ('CONCRETE', "Concrete", "Concrete wall", 'MOD_SOLIDIFY', 2),
            ('WOOD', "Wood", "Wood wall", 'MATERIAL', 3),
            ('CUSTOM', "Custom", "Custom wall type", 'PREFERENCES', 4),
        ],
        default='BASIC'
    )

    # --- Wall Properties ---
    wall_thickness: FloatProperty(
        name="Thickness", default=0.2,
        min=0.01, step=0.01, precision=3, unit='LENGTH'
    )
    wall_height: FloatProperty(
        name="Height", default=2.8,
        min=0.1, step=0.1, precision=2, unit='LENGTH'
    )
    wall_bottom_offset: FloatProperty(
        name="Base Offset", default=0.0,
        min=0.0, step=0.01, precision=3, unit='LENGTH'
    )
    wall_top_offset: FloatProperty(
        name="Top Offset", default=0.0,
        min=0.0, step=0.01, precision=3, unit='LENGTH'
    )
    wall_attach_floor: BoolProperty(
        name="Attach to Floor",
        description="Wall base attaches to floor level",
        default=False
    )
    wall_attach_ceiling: BoolProperty(
        name="Attach to Ceiling",
        description="Wall top attaches to ceiling level",
        default=False
    )
    wall_join_at_end: BoolProperty(
        name="Join at End",
        description="Merge wall ends when closing loop",
        default=True
    )
    wall_material: PointerProperty(
        name="Material", type=bpy.types.Material
    )


class CABINET_OT_edit_wall_type(bpy.types.Operator):
    bl_idname = "cabinet.edit_wall_type"
    bl_label = "Edit Type"
    bl_description = "Edit selected wall type properties"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        self.report({'INFO'}, "Edit Wall Type — Coming Soon")
        return {'FINISHED'}


class VIEW3D_PT_draw_wall_props(bpy.types.Panel):
    bl_label = "Wall"
    bl_idname = "VIEW3D_PT_draw_wall_props"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_HEADER'

    @classmethod
    def poll(cls, context):
        return getattr(context.scene, 'cabinet_active_tool', '') == 'DRAW_WALL'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.cabinet_tool_settings

        # === Start Drawing Button ===
        row = layout.row(align=True)
        row.scale_y = 1.3
        if settings.is_drawing:
            row.alert = True
            row.enabled = False
            row.operator("cabinet.draw_wall", text="⏹ Drawing Active...", icon='PAUSE')
        else:
            row.operator("cabinet.draw_wall", text="▶ Start Drawing", icon='PLAY')

        layout.separator()

        # === Wall Type Selector (Icon Bar) ===
        row = layout.row(align=True)
        row.prop(settings, "wall_type", expand=True)

        # === Edit Type ===
        row = layout.row(align=True)
        row.operator("cabinet.edit_wall_type", text="✏️ Edit Type", icon='GREASEPENCIL')

        layout.separator()

        # === Dimensions ===
        row = layout.row(align=True)
        row.prop(settings, "wall_thickness", text="Thk")
        row.prop(settings, "wall_height", text="Hgt")

        # === Offsets & Attach ===
        row = layout.row(align=True)
        row.prop(settings, "wall_bottom_offset", text="Base Off")
        row.prop(settings, "wall_top_offset", text="Top Off")

        row = layout.row(align=True)
        row.prop(settings, "wall_attach_floor", text="Attach Floor", toggle=True)
        row.prop(settings, "wall_attach_ceiling", text="Attach Ceiling", toggle=True)

        layout.separator()

        # === Material ===
        row = layout.row(align=True)
        row.prop(settings, "wall_material", text="Material")

        # === Join at End ===
        row = layout.row(align=True)
        row.prop(settings, "wall_join_at_end", text="🔗 Join at End", toggle=True)


classes = [
    CabinetToolSettings,
    CABINET_OT_edit_wall_type,
    VIEW3D_PT_draw_wall_props,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cabinet_tool_settings = PointerProperty(type=CabinetToolSettings)
    bpy.types.Scene.cabinet_active_tool = StringProperty(default='NONE')


def unregister():
    try:
        del bpy.types.Scene.cabinet_active_tool
    except AttributeError:
        pass
    try:
        del bpy.types.Scene.cabinet_tool_settings
    except AttributeError:
        pass
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
