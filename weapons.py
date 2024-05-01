#! python3, ursina
#! weapons.py -- entities for different beam variations

import sys, os, time

from ursina import *

from weapon_animator import PowerBeamAnimator, SpeedBeamAnimator, SpreadBeamAnimator, RegularBeamAnimator


#!TODO: -- go through Exceptions and create a log for tracking bugs

class RegularBeam(Entity):
    def __init__(self, player: Entity) -> None:                 # -- Initiates the Regular beam Entity
        super().__init__()
        self.player = player
        self.model: str = "quad"
        self.collider: str = "mesh"
        self.color = color.white
        self.scale: tuple = (.2, 0.2)
        self.position: Vec3 = player.position
        self.z: float = player.z - 0.01
        self.rotation_z: int = player.rotation_z
        self.color = color.rgba(0, 0, 0, 0)
        
        self.dx = 0.8 * math.sin(self.rotation_z / 180 * math.pi)
        self.dy = 0.8 * math.cos(self.rotation_z / 180 * math.pi)
        self.damage: int = 1
        self.beamOrgin = self.position
        self.beamAnimation = RegularBeamAnimator(beam = self)

        # TODO: Figure out issue with blast starting out slow
        
    def firingWeapon(self) -> None:                     # -- Controls beams forward movement
        for beam in self.player.beams:
            if type(beam) != list:
                self.z = self.player.z
                beam.x += beam.dx * time.dt
                beam.y += beam.dy * time.dt
                self.checkDistance(beam)

    def checkDistance(self, beam):                      # -- Checks distance between orgin and current position/removes beam if distance is to far
        differenceX = beam.x - self.beamOrgin.x
        differenceY = beam.y - self.beamOrgin.y
        
        if differenceX >= 10 or differenceX <= -10 or differenceY >= 10 or differenceY <= -10:
            try:
                self.player.beams.remove(beam)
                beam.visible = False
                destroy(beam)
            except Exception as e:
                print(e.__traceback__, "args =", e.args)
            
    def update(self) -> None:                           # -- runs once a frame
        self.firingWeapon()

        if not self.visible:
            destroy(self)


class SpeedBeam(Entity):
    def __init__(self, player: Entity) -> None:                         # -- Initiates Speed beam Entity
        super().__init__()
        self.model: str = "quad"
        self.collider: str = "quad"
        self.scale: tuple = (0.2, 0.2)
        self.position: Vec3 = player.position
        self.z: float = player.z
        self.rotation_z: int = player.rotation_z
        self._always_on_top = False
        self.color = color.rgba(0, 0, 0, 0)

        self.player = player
        self.beamType = "speed"
        self.damage: int = 2
        self.energyConsumption = 1
        self.dx = 0.8 * math.sin(player.rotation_z / 180 * math.pi)
        self.dy = 0.8 * math.cos(player.rotation_z / 180 * math.pi)
        self.beamOrgin: Vec3 = self.position

        ###TEST###
        self.beamAnimation = SpeedBeamAnimator(beam = self)
        ###TEST###

    def firingWeapon(self) -> None:                         # -- Controls beams forward movement
        try:
            for beam in self.player.beams:
                if type(beam) != list:
                    self.z = self.player.z
                    beam.x += beam.dx * time.dt
                    beam.y += beam.dy * time.dt  
                    self.checkDistance(beam)  
        except Exception as e:
            print(e)

    def checkDistance(self, beam) -> None:                        # -- Checks distance between beam and player
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

    def energyDrain(self) -> None:
        if self.player.speedTimerActive:
            self.player.energy -= self.energyConsumption

    def update(self) -> None:                               # -- Runs once per frame
        self.firingWeapon()
        invoke(self.energyDrain, delay = 3)

        if not self.visible:
            try:
                self.disable = True
                self.visible = True
                destroy(self)
            except Exception as e:
                print(e)
            

class SpreadBeam(Entity):
    def __init__(self, player: Entity) -> None:                     # -- Initiates Spread Beam Entity
        super().__init__()
        self.model: str = "quad"                # - Built in variables
        self.collider: str = "quad"
        self.scale: tuple = (0.2, 0.2)
        self.position: Vec3 = player.position
        self.z: float = 1
        self.rotation_z = player.rotation_z
        self._always_on_top = False
        self.color = color.rgba(0, 0, 0, 0)

        self.player = player                    # - Personal variables
        self.beamType = "spread"
        self.damage: int = 2
        self.energyConsumption: float = 1
        self.dx = 0.8 * math.sin(player.rotation_z / 180 * math.pi)
        self.dy = 0.8 * math.cos(player.rotation_z / 180 * math.pi)
        self.beamOrgin: Vec3 = self.position
        self.position.x = self.position.x + ((0.8 * math.sin(self.rotation_z / 180 * math.pi) * 0.5))
        self.position.y = self.position.y + ((0.8 * math.cos(self.rotation_z / 180 * math.pi) * 0.5))
        self.slug: list = []
        self.rotationModifier = 45
        self.beamAnimation = SpreadBeamAnimator(beam = self)

    def firingWeapon(self) -> None:
        for slug in self.player.beams:
            if type(slug) == list:
                for beam in slug:
                    beam.x += (0.8 * math.sin(beam.rotation_z / 180 * math.pi)) * time.dt
                    beam.y += (0.8 * math.cos(beam.rotation_z / 180 * math.pi)) * time.dt

    def checkDistance(self) -> None:
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

    def update(self) -> None:
        self.firingWeapon()
        self.checkDistance()

        if not self.visible:
            try:
                self.disable = True
                self.visible = True
                destroy(self)
            except Exception as e:
                print(e.__traceback__, "args =", e.args)


class PowerBeam(Entity):
    def __init__(self, player: Entity) -> None:                     # -- Initiates Power Beam Entity
        super().__init__()
        self.model: str = "quad"
        self.collider: str = "box"
        self.scale: tuple = (1, 10.5)
        self.position: Vec3 = player.position
        self.z: float = player.z
        self.rotation_z = player.rotation_z
        self._always_on_top = False
        self.visible = True
        self.texture = os.path.join("assets", "player_sprites", "beams", "alpha_model.png")
        self.color = color.rgba(0, 0, 0, 0)

        self.player = player
        self.beamType: str = 'power'
        self.damage: int = 5
        self.energyConsumption: float = 1
        self.dx = 0.8 * math.sin(player.rotation_z / 180 * math.pi)
        self.dy = 0.8 * math.cos(player.rotation_z / 180 * math.pi)
        self.position.x = self.dx 
        self.position.y = self.dy 
        self._always_on_top = False
        self.beamAnimation = PowerBeamAnimator(beam = self)

    def adjustPlacement(self) -> None:
        x = self.player.position.x + ((0.8 * math.sin(self.player.rotation_z / 180 * math.pi) * 7))
        y = self.player.position.y + ((0.8 * math.cos(self.player.rotation_z / 180 * math.pi) * 7))
        z = self.player.position.z
        self.position = Vec3(x, y, z)
        self.rotation_z = self.player.rotation_z

    def beamEnd(self) -> None:
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

    def energyDrain(self) -> None:
        if self.player.powerTimerActive:
            self.player.energy -= self.energyConsumption
            print('drain')

    def update(self) -> None:
        if self.player.powerTimerActive:
            self.adjustPlacement()
            invoke(self.energyDrain, delay = 1)
        else:
            try:
                self.beamEnd()
                destroy(self)
            except:
                pass
        

        ###TEST###
                  # <----Continue here
        

if __name__ == "__main__":
    app = Ursina()
    app.run()