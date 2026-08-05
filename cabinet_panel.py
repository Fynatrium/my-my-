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
    base_dir = os.path.join(addon_dir, "icons", "cabinet")
    sections = {
        "start_design": [
            "smart_box", "pick_interior", "pick_face", "quick_add_board",
            "draw_custom_board", "space_split", "2d_to_3d",
            "create_dimension_driven_parameters", "model_outline"
        ],
        "cabinet_tools": [
            "product_library", "cabinet_generator", "csv_to_door_panel"
        ],
        "edit_tools": [
            "adjust_board", "super_push_pull", "point_range_stretch",
            "set_ab", "mirror_cabinet", "split_back_panel",
            "cabinet_corner_cut", "board_split", "rotate_texture",
            "material_eyedropper", "45_degree_chamfer", "growth_animation",
            "clean_scene", "clean_unused_data", "set_square_data"
        ],
        "door_panel_drawer_tools": [
            "face_to_door_panel", "hide_show", "install_handle"
        ],
        "interactive_animation": [
            "interactive_animation"
        ],
        "annotation_editing": [
            "quick_annotation", "delete_annotation", "quick_set_external_data",
            "set_live_layer", "auto_numbering", "set_one_sided",
            "sorting_code_setting", "panel_pattern_matching"
        ],
        "output_tools": [
            "export_drawings", "upload_installation_drawing"
        ],
    }
    for section, names in sections.items():
        sec_dir = os.path.join(base_dir, section)
        for name in names:
            fp = os.path.join(sec_dir, f"{name}.png")
            if os.path.exists(fp):
                pcoll.load(name, fp, 'IMAGE')
    preview_collections["cabinet"] = pcoll


def get_icon_id(name):
    pcoll = preview_collections.get("cabinet")
    if pcoll and name in pcoll:
        return pcoll[name].icon_id
    return 0


# --- Start Design ---
class CABINET_OT_smart_box(bpy.types.Operator):
    bl_idname = "cabinet.smart_box"
    bl_label = "Smart Box"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Smart Box — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_pick_interior(bpy.types.Operator):
    bl_idname = "cabinet.pick_interior"
    bl_label = "Pick Interior"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Pick Interior — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_pick_face(bpy.types.Operator):
    bl_idname = "cabinet.pick_face"
    bl_label = "Pick Face"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Pick Face — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_quick_add_board(bpy.types.Operator):
    bl_idname = "cabinet.quick_add_board"
    bl_label = "Quick Add Board"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Quick Add Board — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_draw_custom_board(bpy.types.Operator):
    bl_idname = "cabinet.draw_custom_board"
    bl_label = "Draw Custom Board"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Draw Custom Board — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_space_split(bpy.types.Operator):
    bl_idname = "cabinet.space_split"
    bl_label = "Space Split"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Space Split — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_2d_to_3d(bpy.types.Operator):
    bl_idname = "cabinet.2d_to_3d"
    bl_label = "2D to 3D"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "2D to 3D — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_create_dimension_driven_parameters(bpy.types.Operator):
    bl_idname = "cabinet.create_dimension_driven_parameters"
    bl_label = "Create Dimension Driven Parameters"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Create Dimension Driven Parameters — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_model_outline(bpy.types.Operator):
    bl_idname = "cabinet.model_outline"
    bl_label = "Model Outline"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Model Outline — Coming Soon")
        return {'FINISHED'}


# --- Cabinet Tools ---
class CABINET_OT_product_library(bpy.types.Operator):
    bl_idname = "cabinet.product_library"
    bl_label = "Product Library"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Product Library — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_cabinet_generator(bpy.types.Operator):
    bl_idname = "cabinet.cabinet_generator"
    bl_label = "Cabinet Generator"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Cabinet Generator — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_csv_to_door_panel(bpy.types.Operator):
    bl_idname = "cabinet.csv_to_door_panel"
    bl_label = "CSV to Door Panel"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "CSV to Door Panel — Coming Soon")
        return {'FINISHED'}


# --- Edit Tools ---
class CABINET_OT_adjust_board(bpy.types.Operator):
    bl_idname = "cabinet.adjust_board"
    bl_label = "Adjust Board"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Adjust Board — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_super_push_pull(bpy.types.Operator):
    bl_idname = "cabinet.super_push_pull"
    bl_label = "Super Push/Pull"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Super Push/Pull — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_point_range_stretch(bpy.types.Operator):
    bl_idname = "cabinet.point_range_stretch"
    bl_label = "Point/Range Stretch"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Point/Range Stretch — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_set_ab(bpy.types.Operator):
    bl_idname = "cabinet.set_ab"
    bl_label = "Set AB"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Set AB — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_mirror_cabinet(bpy.types.Operator):
    bl_idname = "cabinet.mirror_cabinet"
    bl_label = "Mirror Cabinet"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Mirror Cabinet — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_split_back_panel(bpy.types.Operator):
    bl_idname = "cabinet.split_back_panel"
    bl_label = "Split Back Panel"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Split Back Panel — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_cabinet_corner_cut(bpy.types.Operator):
    bl_idname = "cabinet.cabinet_corner_cut"
    bl_label = "Cabinet Corner Cut"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Cabinet Corner Cut — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_board_split(bpy.types.Operator):
    bl_idname = "cabinet.board_split"
    bl_label = "Board Split"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Board Split — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_rotate_texture(bpy.types.Operator):
    bl_idname = "cabinet.rotate_texture"
    bl_label = "Rotate Texture"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Rotate Texture — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_material_eyedropper(bpy.types.Operator):
    bl_idname = "cabinet.material_eyedropper"
    bl_label = "Material Eyedropper"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Material Eyedropper — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_45_degree_chamfer(bpy.types.Operator):
    bl_idname = "cabinet.45_degree_chamfer"
    bl_label = "45 Degree Chamfer"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "45 Degree Chamfer — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_growth_animation(bpy.types.Operator):
    bl_idname = "cabinet.growth_animation"
    bl_label = "Growth Animation"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Growth Animation — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_clean_scene(bpy.types.Operator):
    bl_idname = "cabinet.clean_scene"
    bl_label = "Clean Scene"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Clean Scene — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_clean_unused_data(bpy.types.Operator):
    bl_idname = "cabinet.clean_unused_data"
    bl_label = "Clean Unused Data"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Clean Unused Data — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_set_square_data(bpy.types.Operator):
    bl_idname = "cabinet.set_square_data"
    bl_label = "Set Square Data"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Set Square Data — Coming Soon")
        return {'FINISHED'}


# --- Door Panel & Drawer Tools ---
class CABINET_OT_face_to_door_panel(bpy.types.Operator):
    bl_idname = "cabinet.face_to_door_panel"
    bl_label = "Face to Door Panel"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Face to Door Panel — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_hide_show(bpy.types.Operator):
    bl_idname = "cabinet.hide_show"
    bl_label = "Hide/Show"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Hide/Show — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_install_handle(bpy.types.Operator):
    bl_idname = "cabinet.install_handle"
    bl_label = "Install Handle"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Install Handle — Coming Soon")
        return {'FINISHED'}


# --- Interactive Animation ---
class CABINET_OT_interactive_animation(bpy.types.Operator):
    bl_idname = "cabinet.interactive_animation"
    bl_label = "Interactive Animation"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Interactive Animation — Coming Soon")
        return {'FINISHED'}


# --- Annotation Editing ---
class CABINET_OT_quick_annotation(bpy.types.Operator):
    bl_idname = "cabinet.quick_annotation"
    bl_label = "Quick Annotation"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Quick Annotation — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_delete_annotation(bpy.types.Operator):
    bl_idname = "cabinet.delete_annotation"
    bl_label = "Delete Annotation"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Delete Annotation — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_quick_set_external_data(bpy.types.Operator):
    bl_idname = "cabinet.quick_set_external_data"
    bl_label = "Quick Set External Data"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Quick Set External Data — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_set_live_layer(bpy.types.Operator):
    bl_idname = "cabinet.set_live_layer"
    bl_label = "Set Live Layer"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Set Live Layer — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_auto_numbering(bpy.types.Operator):
    bl_idname = "cabinet.auto_numbering"
    bl_label = "Auto Numbering"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Auto Numbering — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_set_one_sided(bpy.types.Operator):
    bl_idname = "cabinet.set_one_sided"
    bl_label = "Set One Sided"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Set One Sided — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_sorting_code_setting(bpy.types.Operator):
    bl_idname = "cabinet.sorting_code_setting"
    bl_label = "Sorting Code Setting"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Sorting Code Setting — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_panel_pattern_matching(bpy.types.Operator):
    bl_idname = "cabinet.panel_pattern_matching"
    bl_label = "Panel Pattern Matching"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Panel Pattern Matching — Coming Soon")
        return {'FINISHED'}


# --- Output Tools ---
class CABINET_OT_export_drawings(bpy.types.Operator):
    bl_idname = "cabinet.export_drawings"
    bl_label = "Export Drawings"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Export Drawings — Coming Soon")
        return {'FINISHED'}


class CABINET_OT_upload_installation_drawing(bpy.types.Operator):
    bl_idname = "cabinet.upload_installation_drawing"
    bl_label = "Upload Installation Drawing"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        self.report({'INFO'}, "Upload Installation Drawing — Coming Soon")
        return {'FINISHED'}


class VIEW3D_PT_cabinet_cabinet(bpy.types.Panel):
    bl_label = "Cabinet"
    bl_idname = "VIEW3D_PT_cabinet_cabinet"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cabinet"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 4

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Start Design")
        col = box.column(align=True)
        col.operator("cabinet.smart_box", text="Smart Box", icon='NONE', icon_value=get_icon_id("smart_box"))
        col.operator("cabinet.pick_interior", text="Pick Interior", icon='NONE', icon_value=get_icon_id("pick_interior"))
        col.operator("cabinet.pick_face", text="Pick Face", icon='NONE', icon_value=get_icon_id("pick_face"))
        col.operator("cabinet.quick_add_board", text="Quick Add Board", icon='NONE', icon_value=get_icon_id("quick_add_board"))
        col.operator("cabinet.draw_custom_board", text="Draw Custom Board", icon='NONE', icon_value=get_icon_id("draw_custom_board"))
        col.operator("cabinet.space_split", text="Space Split", icon='NONE', icon_value=get_icon_id("space_split"))
        col.operator("cabinet.2d_to_3d", text="2D to 3D", icon='NONE', icon_value=get_icon_id("2d_to_3d"))
        col.operator("cabinet.create_dimension_driven_parameters", text="Create Dimension Driven Parameters", icon='NONE', icon_value=get_icon_id("create_dimension_driven_parameters"))
        col.operator("cabinet.model_outline", text="Model Outline", icon='NONE', icon_value=get_icon_id("model_outline"))

        box = layout.box()
        box.label(text="Cabinet Tools")
        col = box.column(align=True)
        col.operator("cabinet.product_library", text="Product Library", icon='NONE', icon_value=get_icon_id("product_library"))
        col.operator("cabinet.cabinet_generator", text="Cabinet Generator", icon='NONE', icon_value=get_icon_id("cabinet_generator"))
        col.operator("cabinet.csv_to_door_panel", text="CSV to Door Panel", icon='NONE', icon_value=get_icon_id("csv_to_door_panel"))

        box = layout.box()
        box.label(text="Edit Tools")
        col = box.column(align=True)
        col.operator("cabinet.adjust_board", text="Adjust Board", icon='NONE', icon_value=get_icon_id("adjust_board"))
        col.operator("cabinet.super_push_pull", text="Super Push/Pull", icon='NONE', icon_value=get_icon_id("super_push_pull"))
        col.operator("cabinet.point_range_stretch", text="Point/Range Stretch", icon='NONE', icon_value=get_icon_id("point_range_stretch"))
        col.operator("cabinet.set_ab", text="Set AB", icon='NONE', icon_value=get_icon_id("set_ab"))
        col.operator("cabinet.mirror_cabinet", text="Mirror Cabinet", icon='NONE', icon_value=get_icon_id("mirror_cabinet"))
        col.operator("cabinet.split_back_panel", text="Split Back Panel", icon='NONE', icon_value=get_icon_id("split_back_panel"))
        col.operator("cabinet.cabinet_corner_cut", text="Cabinet Corner Cut", icon='NONE', icon_value=get_icon_id("cabinet_corner_cut"))
        col.operator("cabinet.board_split", text="Board Split", icon='NONE', icon_value=get_icon_id("board_split"))
        col.operator("cabinet.rotate_texture", text="Rotate Texture", icon='NONE', icon_value=get_icon_id("rotate_texture"))
        col.operator("cabinet.material_eyedropper", text="Material Eyedropper", icon='NONE', icon_value=get_icon_id("material_eyedropper"))
        col.operator("cabinet.45_degree_chamfer", text="45 Degree Chamfer", icon='NONE', icon_value=get_icon_id("45_degree_chamfer"))
        col.operator("cabinet.growth_animation", text="Growth Animation", icon='NONE', icon_value=get_icon_id("growth_animation"))
        col.operator("cabinet.clean_scene", text="Clean Scene", icon='NONE', icon_value=get_icon_id("clean_scene"))
        col.operator("cabinet.clean_unused_data", text="Clean Unused Data", icon='NONE', icon_value=get_icon_id("clean_unused_data"))
        col.operator("cabinet.set_square_data", text="Set Square Data", icon='NONE', icon_value=get_icon_id("set_square_data"))

        box = layout.box()
        box.label(text="Door Panel & Drawer Tools")
        col = box.column(align=True)
        col.operator("cabinet.face_to_door_panel", text="Face to Door Panel", icon='NONE', icon_value=get_icon_id("face_to_door_panel"))
        col.operator("cabinet.hide_show", text="Hide/Show", icon='NONE', icon_value=get_icon_id("hide_show"))
        col.operator("cabinet.install_handle", text="Install Handle", icon='NONE', icon_value=get_icon_id("install_handle"))

        box = layout.box()
        box.label(text="Interactive Animation")
        col = box.column(align=True)
        col.operator("cabinet.interactive_animation", text="Interactive Animation", icon='NONE', icon_value=get_icon_id("interactive_animation"))

        box = layout.box()
        box.label(text="Annotation Editing")
        col = box.column(align=True)
        col.operator("cabinet.quick_annotation", text="Quick Annotation", icon='NONE', icon_value=get_icon_id("quick_annotation"))
        col.operator("cabinet.delete_annotation", text="Delete Annotation", icon='NONE', icon_value=get_icon_id("delete_annotation"))
        col.operator("cabinet.quick_set_external_data", text="Quick Set External Data", icon='NONE', icon_value=get_icon_id("quick_set_external_data"))
        col.operator("cabinet.set_live_layer", text="Set Live Layer", icon='NONE', icon_value=get_icon_id("set_live_layer"))
        col.operator("cabinet.auto_numbering", text="Auto Numbering", icon='NONE', icon_value=get_icon_id("auto_numbering"))
        col.operator("cabinet.set_one_sided", text="Set One Sided", icon='NONE', icon_value=get_icon_id("set_one_sided"))
        col.operator("cabinet.sorting_code_setting", text="Sorting Code Setting", icon='NONE', icon_value=get_icon_id("sorting_code_setting"))
        col.operator("cabinet.panel_pattern_matching", text="Panel Pattern Matching", icon='NONE', icon_value=get_icon_id("panel_pattern_matching"))

        box = layout.box()
        box.label(text="Output Tools")
        col = box.column(align=True)
        col.operator("cabinet.export_drawings", text="Export Drawings", icon='NONE', icon_value=get_icon_id("export_drawings"))
        col.operator("cabinet.upload_installation_drawing", text="Upload Installation Drawing", icon='NONE', icon_value=get_icon_id("upload_installation_drawing"))


classes = [
    CABINET_OT_smart_box,
    CABINET_OT_pick_interior,
    CABINET_OT_pick_face,
    CABINET_OT_quick_add_board,
    CABINET_OT_draw_custom_board,
    CABINET_OT_space_split,
    CABINET_OT_2d_to_3d,
    CABINET_OT_create_dimension_driven_parameters,
    CABINET_OT_model_outline,
    CABINET_OT_product_library,
    CABINET_OT_cabinet_generator,
    CABINET_OT_csv_to_door_panel,
    CABINET_OT_adjust_board,
    CABINET_OT_super_push_pull,
    CABINET_OT_point_range_stretch,
    CABINET_OT_set_ab,
    CABINET_OT_mirror_cabinet,
    CABINET_OT_split_back_panel,
    CABINET_OT_cabinet_corner_cut,
    CABINET_OT_board_split,
    CABINET_OT_rotate_texture,
    CABINET_OT_material_eyedropper,
    CABINET_OT_45_degree_chamfer,
    CABINET_OT_growth_animation,
    CABINET_OT_clean_scene,
    CABINET_OT_clean_unused_data,
    CABINET_OT_set_square_data,
    CABINET_OT_face_to_door_panel,
    CABINET_OT_hide_show,
    CABINET_OT_install_handle,
    CABINET_OT_interactive_animation,
    CABINET_OT_quick_annotation,
    CABINET_OT_delete_annotation,
    CABINET_OT_quick_set_external_data,
    CABINET_OT_set_live_layer,
    CABINET_OT_auto_numbering,
    CABINET_OT_set_one_sided,
    CABINET_OT_sorting_code_setting,
    CABINET_OT_panel_pattern_matching,
    CABINET_OT_export_drawings,
    CABINET_OT_upload_installation_drawing,
    VIEW3D_PT_cabinet_cabinet,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    load_icons()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    pcoll = preview_collections.get("cabinet")
    if pcoll:
        bpy.utils.previews.remove(pcoll)
        preview_collections.clear()


if __name__ == "__main__":
    register()