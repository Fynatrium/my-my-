import bpy


class CabinetHistoryItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Display Name", default="")
    op_idname: bpy.props.StringProperty(name="Operator ID", default="")


def add_to_history(op_idname: str, name: str):
    scene = bpy.context.scene
    history = scene.cabinet_often_history
    for i in range(len(history) - 1, -1, -1):
        if history[i].op_idname == op_idname:
            history.remove(i)
            break
    item = history.add(0)
    item.name = name
    item.op_idname = op_idname
    while len(history) > 10:
        history.remove(len(history) - 1)


class CABINET_OT_run_history(bpy.types.Operator):
    bl_idname = "cabinet.run_history"
    bl_label = "Run Tool"
    bl_options = {'REGISTER', 'INTERNAL'}
    op_idname: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        try:
            parts = self.op_idname.split('.')
            op = getattr(bpy.ops, parts[0])
            for part in parts[1:]:
                op = getattr(op, part)
            op('INVOKE_DEFAULT')
        except Exception as e:
            self.report({'WARNING'}, f"Could not run: {e}")
        return {'FINISHED'}


class VIEW3D_PT_cabinet_often(bpy.types.Panel):
    bl_label = "Often"
    bl_idname = "VIEW3D_PT_cabinet_often"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cabinet"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        history = context.scene.cabinet_often_history
        if not history:
            layout.label(text="No recent tools used", icon='INFO')
            return
        grid = layout.grid_flow(columns=2, even_columns=True)
        for item in history:
            op = grid.operator("cabinet.run_history", text=item.name, icon='TOOL_SETTINGS')
            op.op_idname = item.op_idname


classes = [
    CabinetHistoryItem,
    CABINET_OT_run_history,
    VIEW3D_PT_cabinet_often,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cabinet_often_history = bpy.props.CollectionProperty(type=CabinetHistoryItem)


def unregister():
    del bpy.types.Scene.cabinet_often_history
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

