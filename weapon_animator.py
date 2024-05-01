#! python3, ursina
#! weapon_animator.py -- Initiates Weapon Spritesheet Animator entity

import sys, os
from ursina import *


class RegularBeamAnimator(SpriteSheetAnimation):
    def __init__(self, beam: Entity = Entity(), *kwargs) -> None:
        self.texture: str = os.path.join("assets", "player_sprites", "beams", "regular_beam.png")
        self.animations: dict = {
                "regular" : ((0,0), (5,0))
            }
        super().__init__(texture = self.texture, animations = self.animations)
        self.parent: Entity = beam
        self.scale = 8
        self.tileset_size: list = [4, 1]
        self.fps: int = 8

        self.type: str = "regular"
        self.dx: float = 0.8 * math.sin(beam.player.rotation_z / 180 * math.pi)
        self.dy: float = 0.8 * math.cos(beam.player.rotation_z / 180 * math.pi)
        self.position.x = self.dx * 7
        self.position.y = self.dy * 7
        self._always_on_top = True
        self.play_animation("regular")

    def update(self):
        self.rotation_z += 0.1


class PowerBeamAnimator(SpriteSheetAnimation):
    def __init__(self, beam: Entity = Entity(), *kwargs) -> None:           # Initiates Weapons animation spritesheet 
        self.texture: str = os.path.join("assets", "player_sprites", "beams", "power_beam_spritesheet.png")
        self.animations: dict = {
                "power" : ((0,0), (5,0))
            }
        super().__init__(texture = self.texture, animations = self.animations)
        self.parent: Entity = beam
        self.scale = 1
        self.tileset_size: list = [6, 1]
        self.fps: int = 6

        self.type: str = "power"
        self.dx: float = 0.8 * math.sin(beam.player.rotation_z / 180 * math.pi)
        self.dy: float = 0.8 * math.cos(beam.player.rotation_z / 180 * math.pi)
        self.position.x = self.dx * 7
        self.position.y = self.dy * 7
        self._always_on_top = True
        self.play_animation("power")


class SpeedBeamAnimator(SpriteSheetAnimation):
    def __init__(self, beam: Entity = Entity(), *kwargs) -> None:           # Initiates Weapons animation spritesheet 
        self.texture: str = os.path.join("assets", "player_sprites", "beams", "speed_beam.png")
        self.animations: dict = {
                "speed" : ((0 ,0), (5 ,0))
            }
        super().__init__(texture = self.texture, animations = self.animations)
        self.parent: Entity = beam
        self.scale = (3.25, 3)
        self.tileset_size: list = [6, 1]
        self.fps: int = 6

        self.type: str = "speed"
        self.dx: float = 0.8 * math.sin(beam.player.rotation_z / 180 * math.pi)
        self.dy: float = 0.8 * math.cos(beam.player.rotation_z / 180 * math.pi)
        self.position.x = self.dx * 7
        self.position.y = self.dy * 7
        self._always_on_top = True
        self.play_animation("speed")


class SpreadBeamAnimator(SpriteSheetAnimation):
    def __init__(self, beam: Entity = Entity(), *kwargs) -> None:
        self.texture: str = os.path.join("assets", "player_sprites", "beams", "spread_beam.png")
        self.animations: dict = {
                "spread" : ((0 ,0), (5, 0))
            }
        super().__init__(texture = self.texture, animations = self.animations)
        self.parent: Entity = beam
        self.scale: float = (1.75, 1.50)
        self.tileset_size: list = [6, 1]
        self.fps: int = 6

        self.type: str = "spread"
        self.dx: float = 0.8 * math.sin(beam.player.rotation_z / 180 * math.pi)
        self.dy: float = 0.8 * math.cos(beam.player.rotation_z / 180 * math.pi)
        self.position.x = self.dx * 7
        self.position.y = self.dy * 7
        self._always_on_top = True
        self.play_animation("spread")


if __name__ == "__main__":
    app = Ursina()
    y = Entity(player = Entity())
    x = RegularBeamAnimator(beam = y)
    sys.exit(app.run())