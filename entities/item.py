import random
import arcade
from utils.variables import MAP_WIDTH, MAP_HEIGHT

OBJECT_SIZE = 10

class Item(arcade.Sprite):
    def __init__(self):
        # Appeler l'initialisation de la classe parente arcade.Sprite
        super().__init__("resources/images/key.png", scale=1)
        
        # Définir la position après avoir appelé super().__init__()
        self.center_x = random.randint(OBJECT_SIZE, MAP_WIDTH - OBJECT_SIZE)
        self.center_y = random.randint(OBJECT_SIZE, MAP_HEIGHT - OBJECT_SIZE)
        
        self.is_collected = False  # Statut de l'objet (ramassé ou non)
        self.state = "active"  # Ajout de l'état initial "active"

    def delete(self):
        """ Marquer l'objet comme collecté """
        self.is_collected = True
        self.state = "collected"  # Modifier l'état lorsqu'il est ramassé

    def draw(self):
        # Ne dessiner l'objet que s'il n'a pas été ramassé   
        if not self.is_collected:
            super().draw()

    def update_state(self, new_state):
        """Mettre à jour l'état de l'objet (restaurer l'état depuis un checkpoint)"""
        self.state = new_state
        if self.state == "collected":
            self.is_collected = True
        else:
            self.is_collected = False
