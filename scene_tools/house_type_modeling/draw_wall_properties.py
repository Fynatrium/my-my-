import bpy
from bpy.props import (
    FloatProperty, EnumProperty, StringProperty,
    BoolProperty, PointerProperty
)

class CabinetToolSettings(bpy.types.PropertyGroup):
    # --- Snap Settings ---
    wall_snap_mode: EnumProperty(
        name="Snap",
        items=[
            ('NONE', "None", "Free movement"),
            ('ORTHO', "Ortho", "Snap to 90 degrees"),
            ('ANGLE', "Angle", "Snap to custom angle step"),
            ('GRID', "Grid", "Snap to grid"),
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
        name="Bottom Offset", default=0.0,
        min=0.0, step=0.01, precision=3, unit='LENGTH'
    )
    wall_top_offset: FloatProperty(
        name="Top Offset", default=0.0,
        min=0.0, step=0.01, precision=3, unit='LENGTH'
    )
    wall_material: PointerProperty(
        name="Material", type=bpy.types.Material
    )


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

        row = layout.row(align=True)
        row.prop(settings, "wall_thickness", text="Thk")
        row.prop(settings, "wall_height", text="Hgt")
        row.prop(settings, "wall_bottom_offset", text="Bot")
        row.prop(settings, "wall_top_offset", text="Top")
        row.prop(settings, "wall_material", text="")


classes = [
    CabinetToolSettings,
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