#! python3, ursina
#! taget_cursor.py -- a target entity to act as the target for look_at() on player

import sys

from ursina import *



class TargetCursor(Entity):
    def __init__(self) -> None:         # -- Initiates the Target CUrsor entity
        super().__init__()
        self.model = "quad"
        self.scale = 0.5
        self.collider = "mesh"
        self.texture = os.path.join("assets", "target.png")

    def update(self) -> None:           # -- Runs every frame
        print(mouse.world_point)
        (mouse.point)

if __name__ == "__main__":
    app = Ursina()
    target = TargetCursor()
    
    sys.exit(app.run())
           