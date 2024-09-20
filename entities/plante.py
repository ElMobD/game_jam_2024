import arcade
import random
from utils.variables import  MAP_HEIGHT, MAP_WIDTH

class Plante(arcade.Sprite):
    def __init__(self, image, scale=1.0):
        super().__init__(image, scale)
        self.center_x = random.randint(0, MAP_WIDTH)
        self.center_y = random.randint(0, MAP_HEIGHT)
