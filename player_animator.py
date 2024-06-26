#! python3, ursina
#! player_spritesheet.py -- Initiates the Spritesheet for the main character


import sys, os

from ursina import *
from ursina.prefabs.trail_renderer import TrailRenderer

from weapons import RegularBeam, SpeedBeam, SpreadBeam, PowerBeam


class PlayerAnimator(SpriteSheetAnimation):
    def __init__(self, *kwargs) -> None:                                                                # -- Initiates Player Entity
        self.spriteVars()
        self.texture: str = self.spriteTextures["idle"]              # -- Built in variables
        self.animations: dict = self.spriteCommands["idle"]
        super().__init__(texture = self.texture, animations = self.animations)

        self.scale: Vec2 = 1                                        
        self.tileset_size: list = self.tileSize["idle"]
        self.fps: int = 6
        self.always_on_top: bool = True
        self.play_animation("speed")

        self.health: int = 3                                        # -- Private variables
        self.score: int = 0
        self.speed: int = 3
        self.energy: float = 10
        self.currentRotation: float = 0
        self.beams: list = []
        self.type: str = "player"
        self.currentBeam: str = "regular"
        self.currentShipFormation = "speed"

        self.moving = False                                         # -- Triggers
        self.regularTimerActive = False
        self.powerTimerActive = False                               
        self.speedTimerActive = False

    def spriteVars(self) -> None:                                                                       # -- Sets up sprite Sheet dictionaries
        self.spriteTextures = {                                                                         # - SpriteSheet Animations
            "idle" : os.path.join("assets", "player_sprites", "idle", "ship_spritesheet.png"),
            "powerBeamShip" : os.path.join("assets", "player_sprites", "beams", "power_beam_ship_spritesheet.png"),
            "spreadBeamShip" : os.path.join("assets", "player_sprites", "beams", "spread_beam_ship_spritesheet.png"),
            "speedBeamShip" : os.path.join("assets", "player_sprites", "beams", "speed_beam__ship_spritesheet.png"),
            }
        self.spriteCommands: dict = {
            "idle" : { 
                "spread" : ((0, 2), (5, 2)),
                "power" : ((0, 1), (5, 1)),                               
                "speed" : ((0, 0), (5, 0))
            },            
            "ship" : {
                "ship" : ((0, 0), (5, 0))      
            },     
        }
        self.tileSize: dict = {
            "idle" : [6, 3],
            "ship" : [6, 1]
        }

    def spriteController(self, spriteType, beamType = None) -> None:                                     # -- Adjusts active sprite sheets
        if spriteType == "idle":                                    # -- Ship idle animations
            self.texture: str = self.spriteTextures["idle"]
            self.animations: dict = self.spriteCommands["idle"]
            self.scale = 1
            self.tileset_size: list = self.tileSize["idle"]
        
        if spriteType == "ship":                                    # -- Ship beam animations
            if beamType == "power":
                self.texture: str = self.spriteTextures["powerBeamShip"]

            if beamType == "spread":
                self.texture: str = self.spriteTextures["spreadBeamShip"]

            if beamType == "speed":
                self.texture: str = self.spriteTextures["speedBeamShip"]

            self.animations: dict = self.spriteCommands["ship"]
            self.scale = 1
            self.tileset_size: list = self.tileSize["ship"]

    def weaponControls(self) -> None:                                                                   # -- Manages Beam Controls (Power/Speed) wd
        if held_keys["space"] and not self.powerTimerActive:
            if self.currentBeam == "speed" and self.energy >= 1 and not self.speedTimerActive:    # -- Speed beam
                beam = SpeedBeam(self) 
                self.beams.append(beam)
                self.speedTimerActive = True
                invoke(self.checkTimer, delay = 0.1)
                self.spriteController("ship", "speed")

            if self.currentBeam == "power" and self.energy >= 1 and not self.powerTimerActive:    # -- Power beam
                self.powerTimerActive = True
                beamP = PowerBeam(self)
                self.beams.append(beamP)
        else:
            self.spriteController("idle")

    def movement(self) -> None:                                                                         # -- Controls player movement
        velocity: Vec2 = Vec2()                     # -- Player movement vector
        
        if held_keys["w"]:                          # -- Controls player movement and rotation
            velocity.y += self.speed
            self.rotation_z = 0
        
        if held_keys['s']:
            velocity.y -= self.speed
            self.rotation_z = 180

        if held_keys['d']:
            velocity.x += self.speed
            self.rotation_z = 90

        if held_keys['a']:
            velocity.x -= self.speed
            self.rotation_z = 270

        if held_keys['w'] and held_keys['a']:
            self.rotation_z = 315

        if held_keys['w'] and held_keys['d']:
            self.rotation_z = 45

        if held_keys['s'] and held_keys['a']:
            self.rotation_z = 225

        if held_keys['s'] and held_keys['d']:
            self.rotation_z = 135

        self.position += (velocity) * time.dt         # -- Updates player position
    
    def checkTimer(self) -> None:                                                                       # -- Checks player triggers
        if self.regularTimerActive:                                 # -- Regular beam timer
            self.regularTimerActive = False

        if self.powerTimerActive:                                   # -- Power beam timer
            self.powerTimerActive = False

        if self.speedTimerActive:                                   # -- Speed beam timer
            self.speedTimerActive = False

    def meterChecks(self) -> None:                                                                      # -- Checks player meters (health/energy)
        if self.health <= 0:                                        # -- Health Check
            self.visible = False
            self.disable = True

        if self.energy <= 1:                                        # -- Energy Check
            self.checkTimer()                
            self.currentBeam = "regular"                         

    def input(self, key) -> None:                                                                       # -- Validates single button inputs (regular/spread/etc)
        if not self.powerTimerActive:
            if key == 'e':                                              # -- Controls Which beam is active
                self.currentBeam = "regular"

            if key == '1':                  
                self.currentBeam = "speed"
                self.play_animation(self.currentBeam)
            
            if key == '2':
                self.currentBeam = "spread"
                self.play_animation(self.currentBeam)

            if key == '3':
                self.currentBeam = "power"
                self.play_animation(self.currentBeam)

            if key == "space":                                          # -- Controls Beams (Regular/Spread)
                if (self.energy <= 1 or self.currentBeam == "regular") and not self.regularTimerActive:
                    beam = RegularBeam(player = self)
                    self.beams.append(beam)
                    self.regularTimerActive = True
                    invoke(self.checkTimer, delay = 0.25)
                    return

                if self.energy >= 2 and self.currentBeam == "spread":
                    modifiedRotation = -45
                    slug: list = []

                    for _ in range(9):                                  # -- Loads a slug of beams
                        beam = SpreadBeam(self)
                        beam.rotation_z += modifiedRotation
                        slug.append(beam)
                        modifiedRotation += 11.25
                    self.beams.append(slug)
                    self.energy -= beam.energyConsumption
                    self.spriteController("ship", "spread")


        if key == "space up" and self.powerTimerActive:                                       # -- Cancels Power beam
            self.checkTimer()

    def update(self) -> None:                                                                           # -- Updates on every Frame
        self.movement()
        self.weaponControls()
        self.meterChecks()
        
        if self.powerTimerActive:
            self.spriteController("ship", "power")


if __name__ == "__main__":
    app = Ursina()
    EditorCamera()
    bg = Entity(model = "quad", color = color.black, scale = 200, z = 4)
    block = Entity(model = "quad", color = color.green, scale = 1, z = 3)
    player = PlayerAnimator()
    app.run()