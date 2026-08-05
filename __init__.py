bl_info = {
    "name": "Cabinet Maker Pro",
    "author": "User",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > N-Panel > Cabinet",
    "description": "SketchUp-like cabinet builder with grip scaling",
    "category": "Object",
}

import bpy

# Tool options FIRST (properties must exist before operators use them)
from . import tool_options

# Scene tools (operators)
from .scene_tools import house_type_modeling

# Panels
from . import scene_panel
from . import account_panel
from . import often_panel
from . import global_panel
from . import cabinet_panel
from . import report_production_panel
from . import product_library_panel
from . import backend_panel


def register():
    tool_options.register()
    house_type_modeling.register()
    
    scene_panel.register()
    account_panel.register()
    often_panel.register()
    global_panel.register()
    cabinet_panel.register()
    report_production_panel.register()
    product_library_panel.register()
    backend_panel.register()


def unregister():
    backend_panel.unregister()
    product_library_panel.unregister()
    report_production_panel.unregister()
    cabinet_panel.unregister()
    scene_panel.unregister()
    global_panel.unregister()
    often_panel.unregister()
    account_panel.unregister()
    
    house_type_modeling.unregister()
    tool_options.unregister()


if __name__ == "__main__":
    register()
