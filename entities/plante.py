import arcade
import random
from utils.variables import  MAP_HEIGHT, MAP_WIDTH

class Plante(arcade.Sprite):
    def __init__(self, image, scale=1.0,x=None, y=None):
        super().__init__(image, scale)
        if x is not None and y is not None:
            # Si les positions x et y sont spécifiées, les utiliser directement
            self.center_x = x
            self.center_y = y
        else:
            # Sinon, générer des positions aléatoires
            self.center_x = random.randint(0, MAP_WIDTH)
            self.center_y = random.randint(0, MAP_HEIGHT)