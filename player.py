#! python3, ursina
#! player.py -- ursina entity for player character

import sys, os, time

from ursina import *

from weapons import RegularBeam, SpeedBeam, SpreadBeam, PowerBeam
from target_cursor import TargetCursor


class PlayerOne(Sprite):
    def __init__(self) -> None:                                             # -- Initiates the player entity
        ###TEST###
        super().__init__()           
        self.baseSprites = {                                                                         # - SpriteSheet Animations
            "idle" : os.path.join("assets", "player_sprites", "idle", "ship_spritesheet.png"),
            "powerBeamShip" : os.path.join("assets", "player_sprites", "beams", "power_beam_ship_spritesheet.png"),
            "spreadBeamShip" : os.path.join("assets", "player_sprites", "beams", "spread_beam_ship_spritesheet.png"),
            "speedBeamShip" : os.path.join("assets", "player_sprites", "beams", "speed_beam__ship_spritesheet.png"),
            }
        self.tilesetSize: dict = {
            "idle" : [6, 3],
            "powerBeamShip" : [6, 1],
        }
        self.spriteCommands: dict = {
            "idle" : { 
                "spread" : ((0, 2), (5, 2)),
                "power" : ((0, 1), (5, 1)),                               
                "speed" : ((0, 0), (5, 0))
            },            
            "powerBeamShip" : {
                "power" : ((0, 0), (5, 0))      
            },
        }
        self.fps: dict = {
            "idle" : 6,
            "powerBeamShip" : 6,
            } 
        
        self.basic_graphics: SpriteSheetAnimation = SpriteSheetAnimation(
            self.baseSprites["idle"],
            tileset_size = self.tilesetSize["idle"],
            fps = self.fps["idle"],
            animations = self.spriteCommands["idle"]
            )
        
        self.basic_graphics.scale = 1
        self.basic_graphics.z = 3
        
        self.target = Cursor(texture = os.path.join("alpha_assets", "target.png"))      # <- Mouse Cursor
        mouse.visible = True

        self.basic_graphics.play_animation('speed')

        ###TEST###
        EditorCamera()

        self.model: str = "quad"                                                                # - Built in Entity variables
        self.collider: str = "box"
        self.scale: float = 1
        self.z: float = 3
        self.visible = False

        self.health: int = 3                                                                    # - Personal variables
        self.energy: float = 1000
        self.score: int = 0
        self.baseSpeed: int = 3
        self.currentRotation: int = 0
        self.currentBeam: str = "regular"
        self.beams: list = []
        self.currentKey:str = "None"
         
        
        camera.add_script(SmoothFollow(target = self, offset = [0, 1 -30], speed = 4))          # - Camera controls

        self.moving: bool = False           # <- Triggers
        self.regTimerActive: bool = False
        self.speedTimerActive: bool = False
        self.spreadTimerActive: bool = False
        self.powerTimerActive: bool = False
        self.timerList: list = [
            self.regTimerActive, self.speedTimerActive,
            self.spreadTimerActive, self.powerTimerActive,
        ]

        ###TEST###
        

    def input(self, key) -> None:                                           # -- Catches keyboard inputs
    
        if key == "space up":
            self.clearBeamTimer()
        
        if not self.powerTimerActive or not self.spreadTimerActive or not self.speedTimerActive:
            if key == '1' and self.currentBeam != 'speed':
                self.powerTimerActive = False                                                  # - Changes active weapon
                self.currentBeam = "speed"
                self.basic_graphics.play_animation('speed')

            elif key == '2' and self.currentBeam != 'spread':
                self.powerTimerActive = False 
                self.currentBeam = "spread"
                self.basic_graphics.play_animation('spread')

            elif key == '3' and self.currentBeam != 'power':
                self.currentBeam = "power"
                self.basic_graphics.play_animation('power')

            else:
                self.currentBeam == 'regular'
        
        self.currentKey = key
        
    def movementControls(self) -> None:                                     # -- Triggers for movement inputs
        if held_keys['w']:
            if not self.powerTimerActive:
                self.y += self.baseSpeed * time.dt
                self.lookAtCursor()
            
        if held_keys['s']:
            if not self.powerTimerActive:
                self.y -= self.baseSpeed * time.dt
                self.lookAtCursor()

        if held_keys['a']:
            if not self.powerTimerActive:
                self.x -= self.baseSpeed * time.dt
                self.lookAtCursor()
        
        if held_keys['d']:
            if not self.powerTimerActive:
                self.x += self.baseSpeed * time.dt
                self.lookAtCursor()

        if held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']:
            self.moving = True
        else:
            self.moving = False

        self.currentRotation = self.rotation_z
        
    def lookAtCursor(self) -> None:
        self.look_at_2d(self.target)
        self.basic_graphics.look_at_2d(self.target)
        
    def weaponControls(self) -> None:                                        # -- Triggers for weapon inputs 
        if held_keys["space"]:
            if self.energy <= 0 or self.currentBeam == 'regular' and not self.regTimerActive:
                self.clearBeamTimer()
                self.regTimerActive = True
                beam = RegularBeam(self)
                self.beams.append(beam)   
                invoke(self.clearBeamTimer, delay = 0.75)
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
                    self.beams.append(beamP)
                    
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
        if self.energy <= 1:
            self.currentBeam = "regular"

        if self.health <= 0:        # - Catches if player has no health
            self.visible = False

    def updateSpriteSheetPosition(self) -> None:
        self.basic_graphics.position = self.position
        self.basic_graphics.z = 3

    def update(self) -> None:                                              # -- runs once a frame
        self.updateSpriteSheetPosition()
        self.movementControls()
        self.weaponControls()
        self.meterChecks()

        self.lookAtCursor()
        

if __name__ == "__main__":
    
    app = Ursina()
    playerOne = PlayerOne()
    #background = Entity(model = 'quad', texture = "background.png" , scale = 20, z = 4)
    #background.disable = True
    sys.exit(app.run())