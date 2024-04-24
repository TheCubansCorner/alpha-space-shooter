#! python3, ursina
#! weapons.py -- entities for different beam variations


from ursina import *


class RegularBeam(Entity):
    def __init__(self, player) -> None:                 # -- Initiates the Regular beam Entity
        super().__init__()
        self.player = player
        self.damage = 1

        self.model = "quad"
        self.collider = "mesh"
        self.color = rgb(119, 165, 207)
        self.scale = (.2, 0.2)
        self.position = player.position
        self.z = player.z - 0.01
        self.rotation_z = player.rotation_z
        self.dx = 0.8 * math.sin(player.rotation_z / 180 * math.pi)
        self.dy = 0.8 * math.cos(player.rotation_z / 180 * math.pi)

        # TODO: Create delay between shots
        # TODO: Figure out issue with blast starting out slow

    def firingWeapon(self) -> None:                     # -- Controls beams forward movement
        for beam in self.player.beams:
            self.z = self.player.z
            beam.x += beam.dx * time.dt
            beam.y += beam.dy * time.dt

    def update(self) -> None:                   # -- runs once a frame
        self.firingWeapon()