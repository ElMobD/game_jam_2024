import random
import arcade
from utils.variables import MAP_WIDTH, MAP_HEIGHT

OBJECT_SIZE = 10

class Item(arcade.Sprite):
    def __init__(self):
        # Appeler l'initialisation de la classe parente arcade.Sprite
        super().__init__("resources/images/key.png", scale=0.5)
        
        # Définir la position après avoir appelé super().__init__()
        self.center_x = random.randint(OBJECT_SIZE, MAP_WIDTH - OBJECT_SIZE)
        self.center_y = random.randint(OBJECT_SIZE, MAP_HEIGHT - OBJECT_SIZE)
        
        self.is_collected = False  # Statut de l'objet (ramassé ou non)

    def delete(self):
        """ Marquer l'objet comme collecté """
        self.is_collected = True
        self.kill()  # Supprime l'objet de la SpriteList et de l'écran

    def draw(self):
        # Ne dessiner l'objet que s'il n'a pas été ramassé   
        if not self.is_collected:
            #arcade.draw_circle_filled(self.center_x, self.center_y, OBJECT_SIZE, self.color)
            super().draw()

    