import random
import arcade

from variables import MAP_WIDTH, MAP_HEIGHT

OBJECT_SIZE = 10

class Item:
    def __init__(self) -> None:
        self.center_x = random.randint(OBJECT_SIZE, MAP_WIDTH - OBJECT_SIZE)
        self.center_y = random.randint(OBJECT_SIZE, MAP_HEIGHT - OBJECT_SIZE)
        self.color = arcade.color.RED
        
    def draw(self):
        # Dessine la nourriture (un point rouge)
        arcade.draw_circle_filled(self.center_x, self.center_y, OBJECT_SIZE, self.color)