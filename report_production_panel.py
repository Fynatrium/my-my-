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
    base_dir = os.path.join(addon_dir, "icons", "report_production")
    sections = {
        "hardware_craftsmanship": [
            "create_all_hardware", "create_select_hardware", "delete_selected_hardware"
        ],
        "report_management": ["intelligent_detection", "order_management"],
        "project_installation": ["project_management", "installation_diagram"],
        "production_management": ["create_production", "quick_patch", "production_scheduling_system"],
    }
    for section, names in sections.items():
        sec_dir = os.path.join(base_dir, section)
        for name in names:
            fp = os.path.join(sec_dir, f"{name}.png")
            if os.path.exists(fp):
                pcoll.load(name, fp, 'IMAGE')
    preview_collections["report"] = pcoll


def get_icon_id(name):
    pcoll = preview_collections.get("report")
    if pcoll and name in pcoll:
        return pcoll[name].icon_id
    return 0


# --- Hardware Craftsmanship ---
class CABINET_OT_create_all_hardware(bpy.types.Operator):
    bl_idname = "cabinet.create_all_hardware"
    bl_label = "Create All Hardware"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Create All Hardware — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_create_select_hardware(bpy.types.Operator):
    bl_idname = "cabinet.create_select_hardware"
    bl_label = "Create Select Hardware"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Create Select Hardware — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_delete_selected_hardware(bpy.types.Operator):
    bl_idname = "cabinet.delete_selected_hardware"
    bl_label = "Delete Selected Hardware"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Delete Selected Hardware — Coming Soon")
        return {'FINISHED'}


# --- Report Management ---
class CABINET_OT_intelligent_detection(bpy.types.Operator):
    bl_idname = "cabinet.intelligent_detection"
    bl_label = "Intelligent Detection"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Intelligent Detection — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_order_management(bpy.types.Operator):
    bl_idname = "cabinet.order_management"
    bl_label = "Order Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Order Management — Coming Soon")
        return {'FINISHED'}


# --- Project / Installation ---
class CABINET_OT_project_management(bpy.types.Operator):
    bl_idname = "cabinet.project_management"
    bl_label = "Project Management"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Project Management — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_installation_diagram(bpy.types.Operator):
    bl_idname = "cabinet.installation_diagram"
    bl_label = "Installation Diagram"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Installation Diagram — Coming Soon")
        return {'FINISHED'}


# --- Production Management ---
class CABINET_OT_create_production(bpy.types.Operator):
    bl_idname = "cabinet.create_production"
    bl_label = "Create Production"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Create Production — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_quick_patch(bpy.types.Operator):
    bl_idname = "cabinet.quick_patch"
    bl_label = "Quick Patch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Quick Patch — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_production_scheduling_system(bpy.types.Operator):
    bl_idname = "cabinet.production_scheduling_system"
    bl_label = "Production Scheduling System"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Production Scheduling System — Coming Soon")
        return {'FINISHED'}


class VIEW3D_PT_cabinet_report(bpy.types.Panel):
    bl_label = "Report & Production"
    bl_idname = "VIEW3D_PT_cabinet_report"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cabinet"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 5

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Hardware Craftsmanship", icon='TOOL_SETTINGS')
        col = box.column(align=True)
        col.operator("cabinet.create_all_hardware", text="Create All Hardware", icon='ADD', icon_value=get_icon_id("create_all_hardware"))
        col.operator("cabinet.create_select_hardware", text="Create Select Hardware", icon='RESTRICT_SELECT_OFF', icon_value=get_icon_id("create_select_hardware"))
        col.operator("cabinet.delete_selected_hardware", text="Delete Selected Hardware", icon='TRASH', icon_value=get_icon_id("delete_selected_hardware"))

        box = layout.box()
        box.label(text="Report Management", icon='TEXT')
        col = box.column(align=True)
        col.operator("cabinet.intelligent_detection", text="Intelligent Detection", icon='VIEWZOOM', icon_value=get_icon_id("intelligent_detection"))
        col.operator("cabinet.order_management", text="Order Management", icon='FILE_TEXT', icon_value=get_icon_id("order_management"))

        box = layout.box()
        box.label(text="Project / Installation", icon='NONE')
        col = box.column(align=True)
        col.operator("cabinet.project_management", text="Project Management", icon='FILE_FOLDER', icon_value=get_icon_id("project_management"))
        col.operator("cabinet.installation_diagram", text="Installation Diagram", icon='FILE_IMAGE', icon_value=get_icon_id("installation_diagram"))

        box = layout.box()
        box.label(text="Production Management", icon='INDIRECT_ONLY_OFF')
        col = box.column(align=True)
        col.operator("cabinet.create_production", text="Create Production", icon='ADD', icon_value=get_icon_id("create_production"))
        col.operator("cabinet.quick_patch", text="Quick Patch", icon='MODIFIER', icon_value=get_icon_id("quick_patch"))
        col.operator("cabinet.production_scheduling_system", text="Production Scheduling System", icon='TIME', icon_value=get_icon_id("production_scheduling_system"))


classes = [
    CABINET_OT_create_all_hardware,
    CABINET_OT_create_select_hardware,
    CABINET_OT_delete_selected_hardware,
    CABINET_OT_intelligent_detection,
    CABINET_OT_order_management,
    CABINET_OT_project_management,
    CABINET_OT_installation_diagram,
    CABINET_OT_create_production,
    CABINET_OT_quick_patch,
    CABINET_OT_production_scheduling_system,
    VIEW3D_PT_cabinet_report,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    load_icons()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    pcoll = preview_collections.get("report")
    if pcoll:
        bpy.utils.previews.remove(pcoll)
        preview_collections.clear()


if __name__ == "__main__":
    register()

