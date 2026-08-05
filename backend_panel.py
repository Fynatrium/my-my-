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
    base_dir = os.path.join(addon_dir, "icons", "backend")
    sections = {
        "cnc_drill_export_management": [
            "alpha_csv_export", "kdt_export_settings", "banxd_export_settings", "mpr_export_settings",
            "export_csv", "export_side_groove_side_hole", "export_side_hole",
            "exporting_prescription_data", "bpp_export_data_settings", "cix_export_settings",
            "electronic_saw_csv_data", "haode_5_sided_diamond_format_converter",
            "hausel_ptp", "hausel_ptp_1", "log_parser_settings",
            "mortise_and_tenon_output_settings", "mortise_and_tenon_side_holes",
            "ptp_export_settings", "scm_data_export_settings",
            "starry_six_sided_diamond_export_settings", "xianda_six_sided_drill",
            "xiaofeng_data_export_settings"
        ],
        "third_party_software_extensions": [
            "connection_management_j", "exporting_dxf_from_patch", "import_kujiale_data",
            "kujiale_v2", "open_erp", "open_erp_browser_version", "smart_manufacturing_parser"
        ],
        "interconnection_expansion": [
            "la_hole_measurement_post_processing"
        ],
    }
    for section, names in sections.items():
        sec_dir = os.path.join(base_dir, section)
        for name in names:
            fp = os.path.join(sec_dir, f"{name}.png")
            if os.path.exists(fp):
                pcoll.load(name, fp, 'IMAGE')
    preview_collections["backend"] = pcoll


def get_icon_id(name):
    pcoll = preview_collections.get("backend")
    if pcoll and name in pcoll:
        return pcoll[name].icon_id
    return 0


# --- CNC Drill Export Management ---
class CABINET_OT_alpha_csv_export(bpy.types.Operator):
    bl_idname = "cabinet.alpha_csv_export"
    bl_label = "Alpha CSV Export"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Alpha CSV Export — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_kdt_export_settings(bpy.types.Operator):
    bl_idname = "cabinet.kdt_export_settings"
    bl_label = "KDT Export Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "KDT Export Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_banxd_export_settings(bpy.types.Operator):
    bl_idname = "cabinet.banxd_export_settings"
    bl_label = "BANXD Export Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "BANXD Export Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_mpr_export_settings(bpy.types.Operator):
    bl_idname = "cabinet.mpr_export_settings"
    bl_label = "MPR Export Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "MPR Export Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_export_csv(bpy.types.Operator):
    bl_idname = "cabinet.export_csv"
    bl_label = "Export CSV"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Export CSV — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_export_side_groove_side_hole(bpy.types.Operator):
    bl_idname = "cabinet.export_side_groove_side_hole"
    bl_label = "Export Side Groove / Side Hole"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Export Side Groove / Side Hole — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_export_side_hole(bpy.types.Operator):
    bl_idname = "cabinet.export_side_hole"
    bl_label = "Export Side Hole"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Export Side Hole — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_exporting_prescription_data(bpy.types.Operator):
    bl_idname = "cabinet.exporting_prescription_data"
    bl_label = "Exporting Prescription Data"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Exporting Prescription Data — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_bpp_export_data_settings(bpy.types.Operator):
    bl_idname = "cabinet.bpp_export_data_settings"
    bl_label = "BPP Export Data Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "BPP Export Data Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_cix_export_settings(bpy.types.Operator):
    bl_idname = "cabinet.cix_export_settings"
    bl_label = "CIX Export Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "CIX Export Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_electronic_saw_csv_data(bpy.types.Operator):
    bl_idname = "cabinet.electronic_saw_csv_data"
    bl_label = "Electronic Saw CSV Data"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Electronic Saw CSV Data — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_haode_5_sided_diamond_format_converter(bpy.types.Operator):
    bl_idname = "cabinet.haode_5_sided_diamond_format_converter"
    bl_label = "Haode 5-Sided Diamond Format Converter"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Haode 5-Sided Diamond Format Converter — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_hausel_ptp(bpy.types.Operator):
    bl_idname = "cabinet.hausel_ptp"
    bl_label = "Hausel PTP"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Hausel PTP — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_hausel_ptp_1(bpy.types.Operator):
    bl_idname = "cabinet.hausel_ptp_1"
    bl_label = "Hausel PTP 1"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Hausel PTP 1 — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_log_parser_settings(bpy.types.Operator):
    bl_idname = "cabinet.log_parser_settings"
    bl_label = "Log Parser Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Log Parser Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_mortise_and_tenon_output_settings(bpy.types.Operator):
    bl_idname = "cabinet.mortise_and_tenon_output_settings"
    bl_label = "Mortise and Tenon Output Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Mortise and Tenon Output Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_mortise_and_tenon_side_holes(bpy.types.Operator):
    bl_idname = "cabinet.mortise_and_tenon_side_holes"
    bl_label = "Mortise and Tenon Side Holes"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Mortise and Tenon Side Holes — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_ptp_export_settings(bpy.types.Operator):
    bl_idname = "cabinet.ptp_export_settings"
    bl_label = "PTP Export Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "PTP Export Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_scm_data_export_settings(bpy.types.Operator):
    bl_idname = "cabinet.scm_data_export_settings"
    bl_label = "SCM Data Export Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "SCM Data Export Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_starry_six_sided_diamond_export_settings(bpy.types.Operator):
    bl_idname = "cabinet.starry_six_sided_diamond_export_settings"
    bl_label = "Starry Six-Sided Diamond Export Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Starry Six-Sided Diamond Export Settings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_xianda_six_sided_drill(bpy.types.Operator):
    bl_idname = "cabinet.xianda_six_sided_drill"
    bl_label = "Xianda Six-Sided Drill"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Xianda Six-Sided Drill — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_xiaofeng_data_export_settings(bpy.types.Operator):
    bl_idname = "cabinet.xiaofeng_data_export_settings"
    bl_label = "Xiaofeng Data Export Settings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Xiaofeng Data Export Settings — Coming Soon")
        return {'FINISHED'}


# --- Third Party Software Extensions ---
class CABINET_OT_connection_management_j(bpy.types.Operator):
    bl_idname = "cabinet.connection_management_j"
    bl_label = "Connection Management J"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Connection Management J — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_exporting_dxf_from_patch(bpy.types.Operator):
    bl_idname = "cabinet.exporting_dxf_from_patch"
    bl_label = "Exporting DXF from Patch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Exporting DXF from Patch — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_import_kujiale_data(bpy.types.Operator):
    bl_idname = "cabinet.import_kujiale_data"
    bl_label = "Import Kujiale Data"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Import Kujiale Data — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_kujiale_v2(bpy.types.Operator):
    bl_idname = "cabinet.kujiale_v2"
    bl_label = "Kujiale V2"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Kujiale V2 — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_open_erp(bpy.types.Operator):
    bl_idname = "cabinet.open_erp"
    bl_label = "Open ERP"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Open ERP — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_open_erp_browser_version(bpy.types.Operator):
    bl_idname = "cabinet.open_erp_browser_version"
    bl_label = "Open ERP Browser Version"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Open ERP Browser Version — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_smart_manufacturing_parser(bpy.types.Operator):
    bl_idname = "cabinet.smart_manufacturing_parser"
    bl_label = "Smart Manufacturing Parser"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Smart Manufacturing Parser — Coming Soon")
        return {'FINISHED'}


# --- Interconnection Expansion ---
class CABINET_OT_la_hole_measurement_post_processing(bpy.types.Operator):
    bl_idname = "cabinet.la_hole_measurement_post_processing"
    bl_label = "LA Hole Measurement Post Processing"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "LA Hole Measurement Post Processing — Coming Soon")
        return {'FINISHED'}


class VIEW3D_PT_cabinet_backend(bpy.types.Panel):
    bl_label = "Backend"
    bl_idname = "VIEW3D_PT_cabinet_backend"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cabinet"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 8

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="CNC Drill Export Management")
        col = box.column(align=True)
        col.operator("cabinet.alpha_csv_export", text="Alpha CSV Export", icon='NONE', icon_value=get_icon_id("alpha_csv_export"))
        col.operator("cabinet.kdt_export_settings", text="KDT Export Settings", icon='NONE', icon_value=get_icon_id("kdt_export_settings"))
        col.operator("cabinet.banxd_export_settings", text="BANXD Export Settings", icon='NONE', icon_value=get_icon_id("banxd_export_settings"))
        col.operator("cabinet.mpr_export_settings", text="MPR Export Settings", icon='NONE', icon_value=get_icon_id("mpr_export_settings"))
        col.operator("cabinet.export_csv", text="Export CSV", icon='NONE', icon_value=get_icon_id("export_csv"))
        col.operator("cabinet.export_side_groove_side_hole", text="Export Side Groove / Side Hole", icon='NONE', icon_value=get_icon_id("export_side_groove_side_hole"))
        col.operator("cabinet.export_side_hole", text="Export Side Hole", icon='NONE', icon_value=get_icon_id("export_side_hole"))
        col.operator("cabinet.exporting_prescription_data", text="Exporting Prescription Data", icon='NONE', icon_value=get_icon_id("exporting_prescription_data"))
        col.operator("cabinet.bpp_export_data_settings", text="BPP Export Data Settings", icon='NONE', icon_value=get_icon_id("bpp_export_data_settings"))
        col.operator("cabinet.cix_export_settings", text="CIX Export Settings", icon='NONE', icon_value=get_icon_id("cix_export_settings"))
        col.operator("cabinet.electronic_saw_csv_data", text="Electronic Saw CSV Data", icon='NONE', icon_value=get_icon_id("electronic_saw_csv_data"))
        col.operator("cabinet.haode_5_sided_diamond_format_converter", text="Haode 5-Sided Diamond Format Converter", icon='NONE', icon_value=get_icon_id("haode_5_sided_diamond_format_converter"))
        col.operator("cabinet.hausel_ptp", text="Hausel PTP", icon='NONE', icon_value=get_icon_id("hausel_ptp"))
        col.operator("cabinet.hausel_ptp_1", text="Hausel PTP 1", icon='NONE', icon_value=get_icon_id("hausel_ptp_1"))
        col.operator("cabinet.log_parser_settings", text="Log Parser Settings", icon='NONE', icon_value=get_icon_id("log_parser_settings"))
        col.operator("cabinet.mortise_and_tenon_output_settings", text="Mortise and Tenon Output Settings", icon='NONE', icon_value=get_icon_id("mortise_and_tenon_output_settings"))
        col.operator("cabinet.mortise_and_tenon_side_holes", text="Mortise and Tenon Side Holes", icon='NONE', icon_value=get_icon_id("mortise_and_tenon_side_holes"))
        col.operator("cabinet.ptp_export_settings", text="PTP Export Settings", icon='NONE', icon_value=get_icon_id("ptp_export_settings"))
        col.operator("cabinet.scm_data_export_settings", text="SCM Data Export Settings", icon='NONE', icon_value=get_icon_id("scm_data_export_settings"))
        col.operator("cabinet.starry_six_sided_diamond_export_settings", text="Starry Six-Sided Diamond Export Settings", icon='NONE', icon_value=get_icon_id("starry_six_sided_diamond_export_settings"))
        col.operator("cabinet.xianda_six_sided_drill", text="Xianda Six-Sided Drill", icon='NONE', icon_value=get_icon_id("xianda_six_sided_drill"))
        col.operator("cabinet.xiaofeng_data_export_settings", text="Xiaofeng Data Export Settings", icon='NONE', icon_value=get_icon_id("xiaofeng_data_export_settings"))

        box = layout.box()
        box.label(text="Third Party Software Extensions")
        col = box.column(align=True)
        col.operator("cabinet.connection_management_j", text="Connection Management J", icon='NONE', icon_value=get_icon_id("connection_management_j"))
        col.operator("cabinet.exporting_dxf_from_patch", text="Exporting DXF from Patch", icon='NONE', icon_value=get_icon_id("exporting_dxf_from_patch"))
        col.operator("cabinet.import_kujiale_data", text="Import Kujiale Data", icon='NONE', icon_value=get_icon_id("import_kujiale_data"))
        col.operator("cabinet.kujiale_v2", text="Kujiale V2", icon='NONE', icon_value=get_icon_id("kujiale_v2"))
        col.operator("cabinet.open_erp", text="Open ERP", icon='NONE', icon_value=get_icon_id("open_erp"))
        col.operator("cabinet.open_erp_browser_version", text="Open ERP Browser Version", icon='NONE', icon_value=get_icon_id("open_erp_browser_version"))
        col.operator("cabinet.smart_manufacturing_parser", text="Smart Manufacturing Parser", icon='NONE', icon_value=get_icon_id("smart_manufacturing_parser"))

        box = layout.box()
        box.label(text="Interconnection Expansion")
        col = box.column(align=True)
        col.operator("cabinet.la_hole_measurement_post_processing", text="LA Hole Measurement Post Processing", icon='NONE', icon_value=get_icon_id("la_hole_measurement_post_processing"))


classes = [
    CABINET_OT_alpha_csv_export,
    CABINET_OT_kdt_export_settings,
    CABINET_OT_banxd_export_settings,
    CABINET_OT_mpr_export_settings,
    CABINET_OT_export_csv,
    CABINET_OT_export_side_groove_side_hole,
    CABINET_OT_export_side_hole,
    CABINET_OT_exporting_prescription_data,
    CABINET_OT_bpp_export_data_settings,
    CABINET_OT_cix_export_settings,
    CABINET_OT_electronic_saw_csv_data,
    CABINET_OT_haode_5_sided_diamond_format_converter,
    CABINET_OT_hausel_ptp,
    CABINET_OT_hausel_ptp_1,
    CABINET_OT_log_parser_settings,
    CABINET_OT_mortise_and_tenon_output_settings,
    CABINET_OT_mortise_and_tenon_side_holes,
    CABINET_OT_ptp_export_settings,
    CABINET_OT_scm_data_export_settings,
    CABINET_OT_starry_six_sided_diamond_export_settings,
    CABINET_OT_xianda_six_sided_drill,
    CABINET_OT_xiaofeng_data_export_settings,
    CABINET_OT_connection_management_j,
    CABINET_OT_exporting_dxf_from_patch,
    CABINET_OT_import_kujiale_data,
    CABINET_OT_kujiale_v2,
    CABINET_OT_open_erp,
    CABINET_OT_open_erp_browser_version,
    CABINET_OT_smart_manufacturing_parser,
    CABINET_OT_la_hole_measurement_post_processing,
    VIEW3D_PT_cabinet_backend,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    load_icons()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    pcoll = preview_collections.get("backend")
    if pcoll:
        bpy.utils.previews.remove(pcoll)
        preview_collections.clear()


if __name__ == "__main__":
    register()