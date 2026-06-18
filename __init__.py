from .blender import register_blender, unregister_blender
from .ui import register_ui, unregister_ui

# TODO:
# Emissive node tree
# Black/White = alpha node tree
# Focal length/Fov per game (32.987922264627244 for 95 degree in Rat, check WALL-E fov)
# View transform: standard

def register():
    register_blender()
    register_ui()
    return


def unregister():
    unregister_ui()
    unregister_blender()
    return


if __name__ == "__main__":
    register()
