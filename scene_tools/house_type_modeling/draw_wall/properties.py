import bpy
from bpy.props import (
    FloatProperty, EnumProperty, StringProperty,
    BoolProperty, PointerProperty, IntProperty, CollectionProperty
)
from bpy.types import PropertyGroup


LAYER_FUNCTIONS = [
    ('STRUCTURE', "Structure [1]", ""),
    ('SUBSTRATE', "Substrate [2]", ""),
    ('THERMAL', "Thermal/Air [3]", ""),
    ('FINISH1', "Finish 1 [4]", ""),
    ('FINISH2', "Finish 2 [5]", ""),
    ('MEMBRANE', "Membrane", ""),
]


class CabinetWallLayerItem(PropertyGroup):
    function: EnumProperty(name="Function", items=LAYER_FUNCTIONS, default='STRUCTURE')
    material: PointerProperty(name="Material", type=bpy.types.Material)
    thickness: FloatProperty(name="Thickness", default=0.05, min=0.0, step=0.01, precision=3, unit='LENGTH')
    wraps: BoolProperty(name="Wraps", default=False)


class CabinetWallTypeItem(PropertyGroup):
    name: StringProperty(name="Type Name", default="Generic - 200mm")
    family: StringProperty(name="Family", default="Basic Wall")
    thickness: FloatProperty(name="Thickness", default=0.2, unit='LENGTH')
    structure: StringProperty(name="Structure", default="")
    has_layers: BoolProperty(name="Has Custom Layers", default=False)
    layers: CollectionProperty(type=CabinetWallLayerItem)
    active_layer_index: IntProperty(name="Active Layer", default=-1)
    split_layers_as_objects: BoolProperty(
        name="Split Layers as Objects", default=False,
        description="ON = each layer separate mesh. OFF = single mesh with total thickness"
    )


class CabinetLevelItem(PropertyGroup):
    name: StringProperty(name="Level Name", default="Level 1")
    elevation: FloatProperty(name="Elevation", default=0.0, unit='LENGTH')


def _wall_type_enum_items(self, context):
    if context is None:
        return [('0', "None", "")]
    scene = context.scene
    items = []
    for i, wt in enumerate(getattr(scene, 'cabinet_wall_types', [])):
        items.append((str(i), wt.name, f"{wt.family}  |  {wt.thickness:.3f} m"))
    if not items:
        items.append(('0', "No Types", ""))
    return items


def _update_wall_type_enum(self, context):
    try:
        self.wall_type_index = int(self.wall_type_enum)
    except:
        pass


def _level_enum_items(self, context):
    if context is None:
        return [('-1', "Unconnected", "")]
    items = [('-1', "Unconnected", "Free height")]
    for i, lvl in enumerate(getattr(context.scene, 'cabinet_levels', [])):
        items.append((str(i), lvl.name, f"Elev: {lvl.elevation:.2f} m"))
    return items


def _update_base_level_enum(self, context):
    try:
        v = int(self.wall_base_level_enum)
        self.wall_base_level = v
        self.wall_height_mode = 'LEVEL' if v >= 0 else 'UNCONNECTED'
    except:
        pass


def _update_top_level_enum(self, context):
    try:
        v = int(self.wall_top_level_enum)
        self.wall_top_level = v
        if v >= 0:
            self.wall_height_mode = 'LEVEL'
    except:
        pass


class CabinetToolSettings(PropertyGroup):
    is_drawing: BoolProperty(name="Is Drawing", default=False)

    wall_type_index: IntProperty(name="Wall Type", default=0, min=0)
    wall_type_enum: EnumProperty(
        name="Wall Type", items=_wall_type_enum_items, update=_update_wall_type_enum,
    )

    draw_type: EnumProperty(
        name="Draw Type",
        items=[('LINE', "Line", ""), ('RECTANGLE', "Rectangle", ""),
               ('CIRCLE', "Circle", ""), ('PICK_LINE', "Pick Line", "")],
        default='LINE'
    )

    wall_snap_mode: EnumProperty(
        name="Snap",
        items=[('NONE', "None", ""), ('ORTHO', "Ortho", ""),
               ('ANGLE', "Angle", ""), ('GRID', "Grid", "")],
        default='ORTHO'
    )
    wall_ortho_angle: EnumProperty(
        name="Ortho Angle",
        items=[('5', "5°", ""), ('10', "10°", ""), ('15', "15°", ""),
               ('30', "30°", ""), ('45', "45°", ""), ('90', "90°", "")],
        default='90'
    )
    wall_snap_angle: FloatProperty(name="Angle Step", default=90.0, min=1.0, max=180.0, step=5.0)
    wall_grid_size: FloatProperty(name="Grid Size", default=0.1, min=0.001, step=0.01, precision=3, unit='LENGTH')

    wall_location_line: EnumProperty(
        name="Location Line",
        items=[('WALL_CENTER', "Wall Centerline", ""), ('CORE_CENTER', "Core Centerline", ""),
               ('FINISH_EXTERIOR', "Finish Face: Exterior", ""), ('FINISH_INTERIOR', "Finish Face: Interior", ""),
               ('CORE_EXTERIOR', "Core Face: Exterior", ""), ('CORE_INTERIOR', "Core Face: Interior", "")],
        default='WALL_CENTER'
    )
    wall_chain: BoolProperty(name="Chain", default=True)
    wall_offset: FloatProperty(name="Offset", default=0.0, unit='LENGTH')
    wall_offset_flip: BoolProperty(name="Flip Offset", default=False)
    wall_radius: BoolProperty(name="Radius", default=False)
    wall_radius_value: FloatProperty(name="Radius Value", default=0.1, min=0.0, unit='LENGTH')
    wall_even_thickness: BoolProperty(name="Even Thickness", default=True)

    wall_height_mode: EnumProperty(
        name="Height Mode", items=[('UNCONNECTED', "Unconnected", ""), ('LEVEL', "Level", "")],
        default='UNCONNECTED'
    )
    wall_height_direction: EnumProperty(
        name="Direction", items=[('HEIGHT', "Height", ""), ('DEPTH', "Depth", "")],
        default='HEIGHT'
    )

    # Dropdown enums for constraints
    wall_base_level_enum: EnumProperty(
        name="Base Constraint", items=_level_enum_items, update=_update_base_level_enum,
    )
    wall_top_level_enum: EnumProperty(
        name="Top Constraint", items=_level_enum_items, update=_update_top_level_enum,
    )

    # Internal int props (synced by enums)
    wall_base_level: IntProperty(name="Base Level", default=-1)
    wall_top_level: IntProperty(name="Top Level", default=-1)

    wall_unconnected_height: FloatProperty(
        name="Unconnected Height", default=2.8, min=0.1, step=0.1, precision=2, unit='LENGTH'
    )
    wall_bottom_offset: FloatProperty(name="Base Offset", default=0.0, min=0.0, step=0.01, precision=3, unit='LENGTH')
    wall_top_offset: FloatProperty(name="Top Offset", default=0.0, min=0.0, step=0.01, precision=3, unit='LENGTH')

    wall_thickness: FloatProperty(name="Thickness", default=0.2, min=0.01, step=0.01, precision=3, unit='LENGTH')
    wall_height: FloatProperty(name="Height", default=2.8, min=0.1, step=0.1, precision=2, unit='LENGTH')
    wall_material: PointerProperty(name="Material", type=bpy.types.Material)
    wall_manufacturer: StringProperty(name="Manufacturer", default="")
    wall_model: StringProperty(name="Model", default="")
    wall_cost: FloatProperty(name="Cost", default=0.0, precision=2)
    wall_description: StringProperty(name="Description", default="")

    wall_structural: BoolProperty(name="Structural", default=False)
    structural_usage: EnumProperty(
        name="Structural Usage",
        items=[('BEARING', "Bearing", ""), ('NON_BEARING', "Non-bearing", ""), ('SHEAR', "Shear", "")],
        default='BEARING'
    )
    rebar_cover_exterior: StringProperty(name="Rebar Cover - Exterior", default="Rebar Cover 1 <0 cm>")
    rebar_cover_interior: StringProperty(name="Rebar Cover - Interior", default="Rebar Cover 1 <0 cm>")
    rebar_cover_other: StringProperty(name="Rebar Cover - Other", default="Rebar Cover 1 <0 cm>")

    wall_length: FloatProperty(name="Length", default=0.0, unit='LENGTH')
    wall_area: FloatProperty(name="Area", default=0.0, unit='AREA')
    wall_volume: FloatProperty(name="Volume", default=0.0, unit='VOLUME')

    wall_attach_floor: BoolProperty(name="Attach to Floor", default=False)
    wall_attach_ceiling: BoolProperty(name="Attach to Ceiling", default=False)
    base_is_attached: BoolProperty(name="Base is Attached", default=False)
    top_is_attached: BoolProperty(name="Top is Attached", default=False)
    base_extension: FloatProperty(name="Base Extension", default=0.0, unit='LENGTH')
    top_extension: FloatProperty(name="Top Extension", default=0.0, unit='LENGTH')

    room_bounding: BoolProperty(name="Room Bounding", default=True)
    related_to_mass: BoolProperty(name="Related to Mass", default=False)
    cross_section: EnumProperty(
        name="Cross-Section", items=[('VERTICAL', "Vertical", ""), ('SLANTED', "Slanted", "")],
        default='VERTICAL'
    )

    join_status: EnumProperty(
        name="Join Status", items=[('JOINED', "Joined", ""), ('NOT_JOINED', "Not Joined", "")],
        default='JOINED'
    )


def init_default_data(scene):
    if not hasattr(scene, 'cabinet_levels') or len(scene.cabinet_levels) == 0:
        for name, elev in [("Level 1", 0.0), ("Level 2", 3.0), ("Level 3", 6.0), ("Level 4", 9.0), ("Level 5", 12.0)]:
            item = scene.cabinet_levels.add()
            item.name = name
            item.elevation = elev
    if not hasattr(scene, 'cabinet_wall_types') or len(scene.cabinet_wall_types) == 0:
        for name, family, thick in [("Generic - 200mm", "Basic Wall", 0.2), ("Brick - 300mm", "Basic Wall", 0.3), ("Concrete - 400mm", "Basic Wall", 0.4)]:
            item = scene.cabinet_wall_types.add()
            item.name = name
            item.family = family
            item.thickness = thick


def init_default_data_all_scenes(_dummy=None):
    for scene in bpy.data.scenes:
        init_default_data(scene)


classes = [
    CabinetWallLayerItem, CabinetWallTypeItem, CabinetLevelItem, CabinetToolSettings,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cabinet_tool_settings = PointerProperty(type=CabinetToolSettings)
    bpy.types.Scene.cabinet_active_tool = StringProperty(default='NONE')
    bpy.types.Scene.cabinet_levels = CollectionProperty(type=CabinetLevelItem)
    bpy.types.Scene.cabinet_wall_types = CollectionProperty(type=CabinetWallTypeItem)
    bpy.app.handlers.load_post.append(init_default_data_all_scenes)


def unregister():
    if init_default_data_all_scenes in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(init_default_data_all_scenes)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    for attr in ['cabinet_wall_types', 'cabinet_levels', 'cabinet_active_tool', 'cabinet_tool_settings']:
        if hasattr(bpy.types.Scene, attr):
            try:
                delattr(bpy.types.Scene, attr)
            except:
                pass
