from . import draw_wall
# from . import edit_wall
# from . import insert_window
# from . import insert_door
# from . import wall_marking
# from . import arrange_switches
# from . import create_ground
# from . import create_ceiling


def register():
    draw_wall.register()
    # edit_wall.register()
    # insert_window.register()
    # insert_door.register()
    # wall_marking.register()
    # arrange_switches.register()
    # create_ground.register()
    # create_ceiling.register()


def unregister():
    # create_ceiling.unregister()
    # create_ground.unregister()
    # arrange_switches.unregister()
    # wall_marking.unregister()
    # insert_door.unregister()
    # insert_window.unregister()
    # edit_wall.unregister()
    draw_wall.unregister()