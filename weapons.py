#! python3, ursina
#! weapon_animator.py -- Initiates Weapon Spritesheet Animator entity

import sys, os

from ursina import *


class RegularBeam(SpriteSheetAnimation):
    def __init__(self, player: Entity = Entity(), *kwargs) -> None:
        self.texture: str = os.path.join("assets", "player_sprites", "beams", "regular_beam.png")
        self.animations: dict = {
                "regular" : ((0,0), (5,0))
            }
        super().__init__(texture = self.texture, animations = self.animations)
        self.player: SpriteSheetAnimation = player
        self.scale = 1
        self.tileset_size: list = [4, 1]
        self.fps: int = 8
        self.position: Vec3 = player.position
        self.z: float = player.Z
        self.rotation_z = player.rotation_z


        self.type: str = "regular"
        self.dx: float = 0.8 * math.sin(player.rotation_z / 180 * math.pi)
        self.dy: float = 0.8 * math.cos(player.rotation_z / 180 * math.pi)
        self.position.x = self.dx * 7
        self.position.y = self.dy * 7
        self._always_on_top = True
        self.damage: int = 1
        self.delay: int = 1
        self.play_animation("regular")
        self.beamOrgin = player.position

    def firingWeapon(self) -> None:                                     # -- Controls beams forward movement
        for beam in self.player.beams:
            if type(beam) != list:
                self.checkDistance(beam)
                #self.z = self.player.z
                beam.x += beam.dx * time.dt
                beam.y += beam.dy * time.dt

    def update(self) -> None:                                           # -- Updates once a frame
        self.firingWeapon()
        self.rotation_z += 15

        if not self.visible:
            destroy(self)
             
    def checkDistance(self, beam):                                      # -- Checks distance between orgin and current position/removes beam if distance is to far
        differenceX = beam.x - self.beamOrgin.x
        differenceY = beam.y - self.beamOrgin.y
        
        if differenceX >= 10 or differenceX <= -10 or differenceY >= 10 or differenceY <= -10:
            try:
                self.player.beams.remove(beam)
                beam.visible = False
                destroy(beam)
            except Exception as e:
                print(e.__traceback__, "args =", e.args)


class PowerBeam(SpriteSheetAnimation):
    def __init__(self, player: Entity = Entity(), *kwargs) -> None:           # Initiates Weapons animation spritesheet 
        self.texture: str = os.path.join("assets", "player_sprites", "beams", "power_beam_spritesheet.png")
        self.animations: dict = {
                "power" : ((0,0), (5,0))
            }
        super().__init__(texture = self.texture, animations = self.animations)
        self.player: SpriteSheetAnimation = player
        self.scale = (1, 10.5)
        self.tileset_size: list = [6, 1]
        self.fps: int = 6
        self.position: Vec3 = player.position
        self.z: float = player.z
        self.rotation_z: float = player.rotation_z
        self.always_on_top: bool = True


        self.type: str = "power"
        self.damage: int = 5
        self.energyConsumption: float = 1.0
        self.dx: float = 0.8 * math.sin(player.rotation_z / 180 * math.pi)
        self.dy: float = 0.8 * math.cos(player.rotation_z / 180 * math.pi)
        self.position.x = self.dx * 7
        self.position.y = self.dy * 7
        self._always_on_top = True
        self.play_animation("power")

    def adjustPlacement(self) -> None:                                  # -- Adjusts beam position to match player sprite rotation/placement
        x = self.player.position.x + ((0.8 * math.sin(self.player.rotation_z / 180 * math.pi) * 7))
        y = self.player.position.y + ((0.8 * math.cos(self.player.rotation_z / 180 * math.pi) * 7))
        z = self.player.position.z
        self.position = Vec3(x, y, z)
        self.rotation_z = self.player.rotation_z

    def beamEnd(self) -> None:                                          # -- Triggers when beam is deactivated
        self.disable = True
        self.visible = False

        for beam in self.player.beams:      # <- I guess this error is wrong str has no attribute .finished()
            if type(beam) != list:
                try:
                    if not self.player.powerTimerActive:
                        self.player.beams.remove(beam)
                        destroy(beam)
                except Exception as e:
                    print(e)
                    print(e.args)

    def energyDrain(self) -> None:                                      # -- Depletes player energy
        if self.player.powerTimerActive:
            self.player.energy -= self.energyConsumption
            print('drain')

    def update(self) -> None:                                           # -- Updates once per frame
        if self.player.powerTimerActive:
            self.adjustPlacement()
            invoke(self.energyDrain, delay = 1)
        else:
            try:
                self.beamEnd()
                destroy(self)
            except:
                pass


class SpeedBeam(SpriteSheetAnimation):
    def __init__(self, player: Entity = Entity(), *kwargs) -> None:           # Initiates Weapons animation spritesheet 
        self.texture: str = os.path.join("assets", "player_sprites", "beams", "speed_beam.png")
        self.animations: dict = {
                "speed" : ((0 ,0), (5 ,0))
            }
        super().__init__(texture = self.texture, animations = self.animations)
        self.player: SpriteSheetAnimation = player
        self.scale = 1
        self.tileset_size: list = [6, 1]
        self.fps: int = 6
        self.position: Vec3 = player.position
        self.z: float = player.z
        self.rotation_z = player.rotation_z
        self._always_on_top = True

        self.type: str = "speed"
        self.damage: int = 2
        self.energyConsumption: int = 1
        self.dx: float = 0.8 * math.sin(player.rotation_z / 180 * math.pi)
        self.dy: float = 0.8 * math.cos(player.rotation_z / 180 * math.pi)
        self.position.x = self.dx * 7
        self.position.y = self.dy * 7
        self.beamOrgin = self.position
    
        self.play_animation("speed")

    def firingWeapon(self) -> None:                                     # -- Controls beams forward movement
        try:
            for beam in self.player.beams:
                if type(beam) != list:
                    self.z = self.player.z
                    beam.x += beam.dx * time.dt
                    beam.y += beam.dy * time.dt  
                    self.checkDistance(beam)  
        except Exception as e:
                print(e)

    def checkDistance(self, beam) -> None:                              # -- Checks distance between beam and beams start point
        differenceX = beam.x - self.beamOrgin.x
        differenceY = beam.y - self.beamOrgin.y
        difference = (differenceX, differenceY)
        
        try:
            if difference[1] >= 10 or difference[1] <= -10 or difference[0] >= 10 or difference[0] <= -10:
                self.player.beams.remove(beam)
                beam.visible = False
                destroy(beam)
        except Exception as e:
            print(e.__traceback__, "args =", e.args)

    def energyDrain(self) -> None:                                      # -- Depletes player energy
        if self.player.speedTimerActive:
            self.player.energy -= self.energyConsumption

    def update(self) -> None:                                           # -- Updates once per frame
        self.firingWeapon()
        invoke(self.energyDrain, delay = 3)

        if not self.visible:
            try:
                self.disable = True
                self.visible = True
                destroy(self)
            except Exception as e:
                print(e)
            

class SpreadBeam(SpriteSheetAnimation):
    def __init__(self, player: Entity = Entity(), *kwargs) -> None:
        self.texture: str = os.path.join("assets", "player_sprites", "beams", "spread_beam.png")
        self.animations: dict = {
                "spread" : ((0 ,0), (5, 0))
            }
        super().__init__(texture = self.texture, animations = self.animations)
        self.player: SpriteSheetAnimation = player
        self.scale: float = (1.75, 1.50)
        self.tileset_size: list = [6, 1]
        self.fps: int = 6
        self.position: Vec3 = player.position
        self.z = player.Z
        self.rotation_z: float = player.rotation_z
        self.always_on_top = True

        self.type: str = "spread"
        self.damage: int = 2
        self.energyConsumption: float = 1
        self.slug = []
        self.rotationModifier = 45
        self.beamOrgin: Vec3 = player.position
        self.dx: float = 0.8 * math.sin(player.rotation_z / 180 * math.pi)
        self.dy: float = 0.8 * math.cos(player.rotation_z / 180 * math.pi)
        self.position.x = self.dx * 7
        self.position.y = self.dy * 7
        self.play_animation("spread")

    def firingWeapon(self) -> None:                                     # -- Controls beams forward movement
        for slug in self.player.beams:
            if type(slug) == list:
                for beam in slug:
                    beam.x += (0.8 * math.sin(beam.rotation_z / 180 * math.pi)) * time.dt
                    beam.y += (0.8 * math.cos(beam.rotation_z / 180 * math.pi)) * time.dt

    def checkDistance(self) -> None:                                    # -- Checks distance between beam and player and beams start point
        for inx, slug in enumerate(self.player.beams):
            if type(slug) == list:
                for beam in slug:
                    differenceX = beam.position.x - self.beamOrgin.x
                    differenceY = beam.position.y - self.beamOrgin.y

                    try:
                        if differenceX >= 10 or differenceX <= -10 or differenceY >= 10 or differenceY <= -10:
                            self.player.beams[inx].remove(beam)
                            beam.visible = False
                            destroy(beam)
                    except Exception as e:
                        print(e.__traceback__, "args =", e.args)

    def update(self) -> None:                                           # -- Updates once per frame
        self.firingWeapon()
        self.checkDistance()

        if not self.visible:
            try:
                self.disable = True
                self.visible = True
                destroy(self)
            except Exception as e:
                print(e.__traceback__, "args =", e.args)


if __name__ == "__main__":
    app = Ursina()
    y = Entity()
    x = RegularBeam(player = y)
    sys.exit(app.run())