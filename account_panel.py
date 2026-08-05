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
    icons_dir = os.path.join(addon_dir, "icons", "account")
    names = ["profile", "license", "support"]
    for name in names:
        fp = os.path.join(icons_dir, f"{name}.png")
        if os.path.exists(fp):
            pcoll.load(name, fp, 'IMAGE')
    preview_collections["account"] = pcoll


def get_icon_id(name):
    pcoll = preview_collections.get("account")
    if pcoll and name in pcoll:
        return pcoll[name].icon_id
    return 0


class CabinetAccountProperties(bpy.types.PropertyGroup):
    user_name: bpy.props.StringProperty(name="User Name", default="User")
    license_key: bpy.props.StringProperty(name="License Key", default="")


class CABINET_OT_account_profile(bpy.types.Operator):
    bl_idname = "cabinet.account_profile"
    bl_label = "Profile"
    bl_options = {'REGISTER', 'INTERNAL'}
    def execute(self, context):
        self.report({'INFO'}, "Profile — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_account_license(bpy.types.Operator):
    bl_idname = "cabinet.account_license"
    bl_label = "License"
    bl_options = {'REGISTER', 'INTERNAL'}
    def execute(self, context):
        self.report({'INFO'}, "License — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_account_support(bpy.types.Operator):
    bl_idname = "cabinet.account_support"
    bl_label = "Support"
    bl_options = {'REGISTER', 'INTERNAL'}
    def execute(self, context):
        self.report({'INFO'}, "Support — Coming Soon")
        return {'FINISHED'}


class VIEW3D_PT_cabinet_account(bpy.types.Panel):
    bl_label = "Account"
    bl_idname = "VIEW3D_PT_cabinet_account"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cabinet"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        props = context.scene.cabinet_account_props
        col = layout.column(align=True)
        col.prop(props, "user_name")
        col.prop(props, "license_key")
        col.separator()
        col.operator("cabinet.account_profile", text="Profile", icon='USER', icon_value=get_icon_id("profile"))
        col.operator("cabinet.account_license", text="License", icon='KEYINGSET', icon_value=get_icon_id("license"))
        col.operator("cabinet.account_support", text="Support", icon='HELP', icon_value=get_icon_id("support"))


classes = [
    CabinetAccountProperties,
    CABINET_OT_account_profile,
    CABINET_OT_account_license,
    CABINET_OT_account_support,
    VIEW3D_PT_cabinet_account,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cabinet_account_props = bpy.props.PointerProperty(type=CabinetAccountProperties)
    load_icons()


def unregister():
    del bpy.types.Scene.cabinet_account_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    pcoll = preview_collections.get("account")
    if pcoll:
        bpy.utils.previews.remove(pcoll)
        preview_collections.clear()


if __name__ == "__main__":
    register()

