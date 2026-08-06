import bpy


class VIEW3D_PT_draw_wall_modify(bpy.types.Panel):
    bl_label = "Modify"
    bl_idname = "VIEW3D_PT_draw_wall_modify"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOL_HEADER'

    @classmethod
    def poll(cls, context):
        return getattr(context.scene, 'cabinet_active_tool', '') == 'DRAW_WALL'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.cabinet_tool_settings

        row = layout.row(align=True)
        row.prop(settings, "wall_snap_mode", expand=True)

        if settings.wall_snap_mode == 'ANGLE':
            row = layout.row(align=True)
            row.prop(settings, "wall_snap_angle", slider=True)
        elif settings.wall_snap_mode == 'GRID':
            row = layout.row(align=True)
            row.prop(settings, "wall_grid_size")

        layout.separator_spacer()
        layout.prop(settings, "wall_even_thickness", toggle=True)


classes = [
    VIEW3D_PT_draw_wall_modify,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
