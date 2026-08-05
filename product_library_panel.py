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
    base_dir = os.path.join(addon_dir, "icons", "product_library")
    sections = {
        "product_catalog_management": [
            "panel_management", "cabinet_management", "door_panel_management",
            "section_management", "user_gallery", "component_management"
        ],
        "parts_materials": [
            "parts_management", "materials_management"
        ],
        "connector_management": [
            "connector_management", "connection_method_management"
        ],
    }
    for section, names in sections.items():
        sec_dir = os.path.join(base_dir, section)
        for name in names:
            fp = os.path.join(sec_dir, f"{name}.png")
            if os.path.exists(fp):
                pcoll.load(name, fp, 'IMAGE')
    preview_collections["product"] = pcoll


def get_icon_id(name):
    pcoll = preview_collections.get("product")
    if pcoll and name in pcoll:
        return pcoll[name].icon_id
    return 0


class CABINET_OT_panel_management(bpy.types.Operator):
    bl_idname = "cabinet.panel_management"
    bl_label = "Panel Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Panel Management — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_cabinet_management(bpy.types.Operator):
    bl_idname = "cabinet.cabinet_management"
    bl_label = "Cabinet Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Cabinet Management — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_door_panel_management(bpy.types.Operator):
    bl_idname = "cabinet.door_panel_management"
    bl_label = "Door Panel Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Door Panel Management — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_section_management(bpy.types.Operator):
    bl_idname = "cabinet.section_management"
    bl_label = "Section Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Section Management — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_user_gallery(bpy.types.Operator):
    bl_idname = "cabinet.user_gallery"
    bl_label = "User Gallery"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "User Gallery — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_component_management(bpy.types.Operator):
    bl_idname = "cabinet.component_management"
    bl_label = "Component Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Component Management — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_parts_management(bpy.types.Operator):
    bl_idname = "cabinet.parts_management"
    bl_label = "Parts Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Parts Management — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_materials_management(bpy.types.Operator):
    bl_idname = "cabinet.materials_management"
    bl_label = "Materials Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Materials Management — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_connector_management(bpy.types.Operator):
    bl_idname = "cabinet.connector_management"
    bl_label = "Connector Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Connector Management — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_connection_method_management(bpy.types.Operator):
    bl_idname = "cabinet.connection_method_management"
    bl_label = "Connection Method Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Connection Method Management — Coming Soon")
        return {'FINISHED'}


class VIEW3D_PT_cabinet_product_library(bpy.types.Panel):
    bl_label = "Product Library Management"
    bl_idname = "VIEW3D_PT_cabinet_product_library"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cabinet"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 7

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Product Catalog Management", icon='ASSET_MANAGER')
        col = box.column(align=True)
        col.operator("cabinet.panel_management", text="Panel Management", icon='MESH_PLANE', icon_value=get_icon_id("panel_management"))
        col.operator("cabinet.cabinet_management", text="Cabinet Management", icon='CUBE', icon_value=get_icon_id("cabinet_management"))
        col.operator("cabinet.door_panel_management", text="Door Panel Management", icon='MOD_SOLIDIFY', icon_value=get_icon_id("door_panel_management"))
        col.operator("cabinet.section_management", text="Section Management", icon='MODIFIER', icon_value=get_icon_id("section_management"))
        col.operator("cabinet.user_gallery", text="User Gallery", icon='IMAGE_BACKGROUND', icon_value=get_icon_id("user_gallery"))
        col.operator("cabinet.component_management", text="Component Management", icon='OUTLINER_OB_MESH', icon_value=get_icon_id("component_management"))

        box = layout.box()
        box.label(text="Parts / Materials", icon='NONE')
        col = box.column(align=True)
        col.operator("cabinet.parts_management", text="Parts Management", icon='PARTICLES', icon_value=get_icon_id("parts_management"))
        col.operator("cabinet.materials_management", text="Materials Management", icon='MATERIAL', icon_value=get_icon_id("materials_management"))

        box = layout.box()
        box.label(text="Connector Management", icon='NONE')
        col = box.column(align=True)
        col.operator("cabinet.connector_management", text="Connector Management", icon='MODIFIER', icon_value=get_icon_id("connector_management"))
        col.operator("cabinet.connection_method_management", text="Connection Method Management", icon='MODIFIER', icon_value=get_icon_id("connection_method_management"))


classes = [
    CABINET_OT_panel_management,
    CABINET_OT_cabinet_management,
    CABINET_OT_door_panel_management,
    CABINET_OT_section_management,
    CABINET_OT_user_gallery,
    CABINET_OT_component_management,
    CABINET_OT_parts_management,
    CABINET_OT_materials_management,
    CABINET_OT_connector_management,
    CABINET_OT_connection_method_management,
    VIEW3D_PT_cabinet_product_library,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    load_icons()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    pcoll = preview_collections.get("product")
    if pcoll:
        bpy.utils.previews.remove(pcoll)
        preview_collections.clear()


if __name__ == "__main__":
    register()

