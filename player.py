#! python3, ursina
#! player.py -- ursina entity for player character

import sys, os, time

from ursina import *

from weapons import RegularBeam, SpeedBeam, SpreadBeam, PowerBeam
from target_cursor import TargetCursor


class PlayerOne(Entity):
    def __init__(self) -> None:                                             # -- Initiates the player entity
        super().__init__()
        self.model: str = "quad"
        self.collider: str = "mesh"
        self.scale: float = 1
        self.texture: str = os.path.join("assets", "speed_form.png")
        self.z: float = 3

        self.health: int = 3
        self.energy: float = 50
        self.score: int = 0
        self.baseSpeed: int = 3
        self.currentRotation: int = 0
        self.currentBeam: str = "regular"
        self.beams: list = []
        self.currentKey:str = "None"
        
        camera.add_script(SmoothFollow(target = self, offset = [0, 1 -30], speed = 4))

        self.moving: bool = False           # <- Triggers
        self.regTimerActive: bool = False
        self.speedTimerActive: bool = False
        self.spreadTimerActive: bool = False
        self.powerTimerActive: bool = False

    def input(self, key) -> None:                                           # -- Catches keyboard inputs
        if key == "space up":
            self.clearBeamTimer()
            
        if key == '1' and self.currentBeam != 'speed':                                                  # - Changes active weapon
            self.clearBeamTimer()
            self.currentBeam = "speed"
            self.texture = os.path.join("assets", "speed_form.png")
        elif key == '2' and self.currentBeam != 'spread':
            self.clearBeamTimer()
            self.currentBeam = "spread"
            self.texture = os.path.join("assets", "spread_form.png")
        elif key == '3' and self.currentBeam != 'power':
            self.clearBeamTimer()
            self.currentBeam = "power"
            self.texture = os.path.join("assets", "power_form.png")
        else:
            self.clearBeamTimer()
            self.currentBeam == 'regular'
        
        self.currentKey = key
        
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
        

    def weaponControls(self) -> None:                                        # -- Triggers for weapon inputs
        if held_keys["space"]:
            if (self.energy <= 0 or self.currentBeam == 'regular') and not self.regTimerActive:
                self.clearBeamTimer()
                self.regTimerActive = True
                invoke(self.clearBeamTimer, delay = 0.5)
                beam = RegularBeam(self)
                self.beams.append(beam)   

            else: 
                if self.currentBeam == "speed" and not self.speedTimerActive and self.energy >= 0.2:
                    self.speedTimerActive = True
                    invoke(self.clearBeamTimer, delay = 0.1)
                    beam = SpeedBeam(self)
                    self.beams.append(beam)
                    self.energy -= beam.energyConsumption  
 
                if self.currentBeam == "spread" and not self.spreadTimerActive and self.energy >= 1.5:
                    self.spreadTimerActive = True
                    invoke(self.clearBeamTimer, delay = 1)
                    modifiedRotation = -45
                    slug: list = []

                    for _ in range(9):                      # - Loads a slug of beams
                        beam = SpreadBeam(self)
                        beam.rotation_z += modifiedRotation
                        slug.append(beam)
                        modifiedRotation += 11.25
                    self.beams.append(slug)
                    self.energy -= beam.energyConsumption
                
                if self.currentBeam == "power" and not self.powerTimerActive and self.energy >= 3.0:
                    self.powerTimerActive = True
                    beamP = PowerBeam(self)

    def clearBeamTimer(self) -> None:
        if self.currentBeam == "regular":
            self.regTimerActive = False
        
        if self.currentBeam == "speed":
            self.speedTimerActive = False

        if self.currentBeam == "spread":
            self.spreadTimerActive = False

        if self.currentBeam == "power":
            self.powerTimerActive = False

    def meterChecks(self) -> None:
        if self.energy < 0.2:
            self.currentBeam = "regular"

        if self.energy < 0.2:
            self.energy = 0

        if self.health == 0:        # - Catches if player has no health
            self.visible = False

    def update(self) -> None:                                               # -- runs once a frame
        self.movementControls()
        self.weaponControls()
        self.meterChecks()
        

if __name__ == "__main__":
    
    app = Ursina()
    playerOne = PlayerOne()
    sys.exit(app.run())