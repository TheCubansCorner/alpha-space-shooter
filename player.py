#! python3, ursina
#! player.py -- ursina entity for player character

import sys, os

from ursina import *

from weapons import RegularBeam


class PlayerOne(Entity):
    def __init__(self) -> None:                                             # -- Initiates the player entity
        super().__init__()
        self.model: str = "quad"
        self.collider: str = "mesh"
        self.scale: float = 1
        self.texture: str = os.path.join("assets", "speed_form.png")
        self.z: float = 3

        self.health: int = 3
        self.energy: int = 0
        self.score: int = 0
        self.baseSpeed: int = 3
        self.currentRotation: int = 0
        self.currentBeam: str = "regular"
        self.moving: bool = False
        self.beams: list = []

    def input(self, key) -> None:                                           # -- Catches keyboard inputs
        if key == '1':                                                  # - Changes active weapon
            self.currentBeam = "speed"
            self.texture = os.path.join("assets", "speed_form.png")

        if key == '2':
            self.currentBeam = "spread"
            self.texture = os.path.join("assets", "spread_form.png")

        if key == '3':
            self.currentBeam = "power"
            self.texture = os.path.join("assets", "power_form.png")

        if self.energy == 0:
            if key == "space":
                beam = RegularBeam(self)
                self.beams.append(beam)
                self.currentBeam = "regular"
        else:
            pass

    def movementControls(self) -> None:                                     # -- Triggers for movement inputs
        if held_keys['w']:
            self.rotation_z = 0
            self.y += self.baseSpeed * time.dt
            
        if held_keys['s']:
            self.rotation_z = 180
            self.y -= self.baseSpeed * time.dt

        if held_keys['a']:
            self.rotation_z = 270
            self.x -= self.baseSpeed * time.dt
        
        if held_keys['d']:
            self.rotation_z = 90
            self.x += self.baseSpeed * time.dt

        if held_keys['w'] and held_keys['a']:
            self.rotation_z = 315

        if held_keys['w'] and held_keys['d']:
            self.rotation_z = 45

        if held_keys['s'] and held_keys['a']:
            self.rotation_z = 225
        
        if held_keys['s'] and held_keys['d']:
            self.rotation_z = 135

        if held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']:
            self.moving = True
        else:
            self.moving = False

        self.currentRotation = self.rotation_z

    def update(self) -> None:                                               # -- runs once a frame
        self.movementControls()

        if self.health == 0:        # - Catches if player has no health
            self.visible = False

if __name__ == "__main__":
    app = Ursina()
    playerOne = PlayerOne()
    sys.exit(app.run())