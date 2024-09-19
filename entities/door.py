import arcade
from utils.variables import MAP_WIDTH, MAP_HEIGHT

class Door(arcade.Sprite):
    def __init__(self, x, y):
        # Charger l'image de la porte
        super().__init__("resources/images/door.png", scale=3)
        
        # Placer la porte à une position spécifique
        self.center_x = x
        self.center_y = y

    def draw(self):
        """Dessiner la porte sur la map"""
        super().draw()
