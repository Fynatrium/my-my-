import bpy
import os
import bpy.utils.previews

preview_collections = {}


def load_icons():
    pcoll = bpy.utils.previews.new()
    try:
        addon_dir = os.path.dirname(__file__)
    except NameError:
        addon_dir = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else ""
    base_dir = os.path.join(addon_dir, "icons", "global")
    sections = {
        "global_settings_and_pricing": [
            "system_settings", "global_parameters", "quotation_management", "control"
        ],
    }
    for section, names in sections.items():
        sec_dir = os.path.join(base_dir, section)
        for name in names:
            fp = os.path.join(sec_dir, f"{name}.png")
            if os.path.exists(fp):
                pcoll.load(name, fp, 'IMAGE')
    preview_collections["global"] = pcoll


def get_icon_id(name):
    pcoll = preview_collections.get("global")
    if pcoll and name in pcoll:
        return pcoll[name].icon_id
    return 0


class CABINET_OT_global_system_settings(bpy.types.Operator):
    bl_idname = "cabinet.global_system_settings"
    bl_label = "System Settings"
    bl_options = {'REGISTER', 'INTERNAL'}
    def execute(self, context):
        self.report({'INFO'}, "System Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_global_parameters(bpy.types.Operator):
    bl_idname = "cabinet.global_parameters"
    bl_label = "Global Parameters"
    bl_options = {'REGISTER', 'INTERNAL'}
    def execute(self, context):
        self.report({'INFO'}, "Global Parameters — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_global_quotation(bpy.types.Operator):
    bl_idname = "cabinet.global_quotation"
    bl_label = "Quotation Management"
    bl_options = {'REGISTER', 'INTERNAL'}
    def execute(self, context):
        self.report({'INFO'}, "Quotation Management — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_global_control(bpy.types.Operator):
    bl_idname = "cabinet.global_control"
    bl_label = "Control"
    bl_options = {'REGISTER', 'INTERNAL'}
    def execute(self, context):
        self.report({'INFO'}, "Control — Coming Soon")
        return {'FINISHED'}


class VIEW3D_PT_cabinet_global(bpy.types.Panel):
    bl_label = "Global"
    bl_idname = "VIEW3D_PT_cabinet_global"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cabinet"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Global Settings and Pricing", icon='WORLD')
        col = box.column(align=True)
        col.operator("cabinet.global_system_settings", text="System Settings", icon='PREFERENCES', icon_value=get_icon_id("system_settings"))
        col.operator("cabinet.global_parameters", text="Global Parameters", icon='PREFERENCES', icon_value=get_icon_id("global_parameters"))
        col.operator("cabinet.global_quotation", text="Quotation Management", icon='PREFERENCES', icon_value=get_icon_id("quotation_management"))
        col.operator("cabinet.global_control", text="Control", icon='PREFERENCES', icon_value=get_icon_id("control"))


classes = [
    CABINET_OT_global_system_settings,
    CABINET_OT_global_parameters,
    CABINET_OT_global_quotation,
    CABINET_OT_global_control,
    VIEW3D_PT_cabinet_global,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    load_icons()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    pcoll = preview_collections.get("global")
    if pcoll:
        bpy.utils.previews.remove(pcoll)
        preview_collections.clear()


if __name__ == "__main__":
    register()

