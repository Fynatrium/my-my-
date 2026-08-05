import bpy
from bpy.props import FloatProperty, EnumProperty, StringProperty


class CabinetToolSettings(bpy.types.PropertyGroup):
    wall_thickness: FloatProperty(name="Thickness", default=0.2, min=0.01, step=0.01, precision=3, unit='LENGTH')
    wall_height: FloatProperty(name="Height", default=2.8, min=0.1, step=0.1, precision=2, unit='LENGTH')
    wall_snap_mode: EnumProperty(
        name="Snap Mode",
        items=[
            ('NONE', "None", "Free movement"),
            ('ORTHO', "Ortho", "Snap to 90 degrees"),
            ('ANGLE', "Angle", "Snap to custom angle step"),
            ('GRID', "Grid", "Snap to grid"),
        ],
        default='ORTHO'
    )
    wall_snap_angle: FloatProperty(name="Angle Step", default=90.0, min=1.0, max=180.0, step=5.0)
    wall_grid_size: FloatProperty(name="Grid Size", default=0.1, min=0.001, step=0.01, precision=3, unit='LENGTH')
    wall_even_thickness: bpy.props.BoolProperty(name="Even Thickness", description="Maintain even wall thickness at corners", default=True)


class VIEW3D_PT_cabinet_tool_options(bpy.types.Panel):
    bl_label = "Tool Options"
    bl_idname = "VIEW3D_PT_cabinet_tool_options"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Cabinet"
    bl_order = 0
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.cabinet_tool_settings
        active_tool = getattr(context.scene, 'cabinet_active_tool', 'NONE')
        
        if active_tool == 'DRAW_WALL':
            self._draw_wall_ui(layout, settings)
        elif active_tool == 'EDIT_WALL':
            self._draw_edit_wall_ui(layout, settings)
        else:
            box = layout.box()
            box.label(text="No Tool Active", icon='INFO')
            box.label(text="Select a tool from")
            box.label(text="the Cabinet panel")
    
    def _draw_wall_ui(self, layout, settings):
        box = layout.box()
        box.label(text="Wall Settings", icon='NONE')
        col = box.column(align=True)
        col.prop(settings, "wall_thickness")
        col.prop(settings, "wall_height")
        box.separator()
        box.prop(settings, "wall_even_thickness", toggle=True)
        box.separator()
        box.label(text="Snap Mode:")
        row = box.row(align=True)
        row.prop(settings, "wall_snap_mode", expand=True)
        if settings.wall_snap_mode == 'ANGLE':
            box.prop(settings, "wall_snap_angle", slider=True)
        elif settings.wall_snap_mode == 'GRID':
            box.prop(settings, "wall_grid_size")
    
    def _draw_edit_wall_ui(self, layout, settings):
        box = layout.box()
        box.label(text="Edit Wall", icon='NONE')
        box.label(text="Coming Soon...")


classes = [
    CabinetToolSettings,
    VIEW3D_PT_cabinet_tool_options,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cabinet_tool_settings = bpy.props.PointerProperty(type=CabinetToolSettings)
    bpy.types.Scene.cabinet_active_tool = StringProperty(default='NONE')


def unregister():
    del bpy.types.Scene.cabinet_active_tool
    del bpy.types.Scene.cabinet_tool_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()