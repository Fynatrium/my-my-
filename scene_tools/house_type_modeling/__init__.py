from . import draw_wall_properties
from . import draw_wall_modifier
from . import draw_wall

def register():
    draw_wall_properties.register()
    draw_wall_modifier.register()
    draw_wall.register()

def unregister():
    draw_wall.unregister()
    draw_wall_modifier.unregister()
    draw_wall_properties.unregister()
