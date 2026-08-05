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
    base_dir = os.path.join(addon_dir, "icons", "scene")
    sections = {
        "house_type_modeling": [
            "draw_wall", "edit_wall", "insert_window", "insert_door",
            "wall_marking", "arrange_switches", "create_ground", "create_ceiling"
        ],
        "kitchen_countertop": ["draw_tabletop", "place_sink"],
        "accessory_model": ["wooden_model"],
    }
    for section, names in sections.items():
        sec_dir = os.path.join(base_dir, section)
        for name in names:
            fp = os.path.join(sec_dir, f"{name}.png")
            if os.path.exists(fp):
                pcoll.load(name, fp, 'IMAGE')
    preview_collections["scene"] = pcoll


def get_icon_id(name):
    pcoll = preview_collections.get("scene")
    if pcoll and name in pcoll:
        return pcoll[name].icon_id
    return 0


class VIEW3D_PT_cabinet_scene(bpy.types.Panel):
    bl_label = "Scene"
    bl_idname = "VIEW3D_PT_cabinet_scene"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cabinet"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 3

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="House Type Modeling", icon='NONE')
        col = box.column(align=True)
        col.operator("cabinet.draw_wall", text="Draw Wall", icon='NONE', icon_value=get_icon_id("draw_wall"))
        col.operator("cabinet.edit_wall", text="Edit Wall", icon='NONE', icon_value=get_icon_id("edit_wall"))
        col.operator("cabinet.insert_window", text="Insert Window", icon='NONE', icon_value=get_icon_id("insert_window"))
        col.operator("cabinet.insert_door", text="Insert Door", icon='NONE', icon_value=get_icon_id("insert_door"))
        col.operator("cabinet.wall_marking", text="Wall Marking", icon='NONE', icon_value=get_icon_id("wall_marking"))
        col.operator("cabinet.arrange_switches", text="Arrange Switches", icon='NONE', icon_value=get_icon_id("arrange_switches"))
        col.operator("cabinet.create_ground", text="Create Ground", icon='NONE', icon_value=get_icon_id("create_ground"))
        col.operator("cabinet.create_ceiling", text="Create Ceiling", icon='NONE', icon_value=get_icon_id("create_ceiling"))

        box = layout.box()
        box.label(text="Kitchen Countertop", icon='NONE')
        col = box.column(align=True)
        col.operator("cabinet.draw_tabletop", text="Draw Tabletop", icon='NONE', icon_value=get_icon_id("draw_tabletop"))
        col.operator("cabinet.place_sink", text="Place Sink", icon='NONE', icon_value=get_icon_id("place_sink"))

        box = layout.box()
        box.label(text="Accessory Model", icon='NONE')
        col = box.column(align=True)
        col.operator("cabinet.wooden_model", text="Wooden Model", icon='NONE', icon_value=get_icon_id("wooden_model"))


classes = [
    VIEW3D_PT_cabinet_scene,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    load_icons()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    pcoll = preview_collections.get("scene")
    if pcoll:
        bpy.utils.previews.remove(pcoll)
        preview_collections.clear()


if __name__ == "__main__":
    register()