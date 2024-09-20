import random
import arcade
from utils.variables import MAP_WIDTH, MAP_HEIGHT

class Hourglass(arcade.Sprite):
    def __init__(self):
        # Appeler l'initialisation de la classe parente arcade.Sprite
        super().__init__("resources/images/hourglass.png", scale=1)
        
        # Définir la position du sablier
        self.center_x = random.randint(50, MAP_WIDTH - 50)
        self.center_y = random.randint(50, MAP_HEIGHT - 50)
        
        self.is_collected = False  # Statut du sablier (ramassé ou non)

    def delete(self):
        """ Marquer le sablier comme collecté """
        self.is_collected = True

    def draw(self):
        # Ne dessiner le sablier que s'il n'a pas été ramassé
        if not self.is_collected:
            super().draw()