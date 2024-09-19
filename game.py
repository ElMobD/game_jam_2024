import arcade
from entities.item import Item
import random
import math

from utils.variables import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MAP_HEIGHT, MAP_WIDTH, PLAYER_MOVEMENT_SPEED, DISTANCE_LIMIT_HELP

DISTANCE_LIMIT_HELP = 300  # Tolérance pour l'affichage des flèches
ARROW_OFFSET = 100  # Décalage pour dessiner la flèche
ARROW_SIZE = 20  # Taille de la flèche


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Charger l'image de fond
        self.background = arcade.load_texture("test.png")
        
        # Créer le joueur
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", scale=0.5)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        
        # Créer une liste de sprites pour le joueur
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Configurer la caméra
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Liste des objets
        self.items = []

    def on_draw(self):
        """ Fonction d'affichage """
        arcade.start_render()

        # Appliquer la caméra
        self.camera.use()

        # Dessiner le fond (les coordonnées 0, 0 sont en bas à gauche)
        arcade.draw_lrwh_rectangle_textured(0, 0, MAP_WIDTH, MAP_HEIGHT, self.background)
        
        # Dessiner le joueur
        self.player_list.draw()

        for item in self.items:
            item.draw()
            
        # Dessiner les flèches si le joueur est trop éloigné des items
        for item in self.items:
            self.draw_arrow_to_item(item)


    def draw_arrow_to_item(self, item):
        """Dessine une flèche pointant vers l'item si trop loin du joueur"""

        # Calculer la distance entre le joueur et l'item
        distance_x = item.center_x - self.player_sprite.center_x
        distance_y = item.center_y - self.player_sprite.center_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if distance > DISTANCE_LIMIT_HELP:
            # Calculer l'angle pour déterminer la direction
            angle = math.atan2(distance_y, distance_x)
            
            # Calculer les coordonnées pour dessiner la flèche
            arrow_x = self.player_sprite.center_x + ARROW_OFFSET * math.cos(angle)
            arrow_y = self.player_sprite.center_y + ARROW_OFFSET * math.sin(angle)
            
            # Calculer les coordonnées des points de la flèche
            end_x = arrow_x
            end_y = arrow_y
            left_x = end_x - ARROW_SIZE * math.cos(angle + math.pi / 6)
            left_y = end_y - ARROW_SIZE * math.sin(angle + math.pi / 6)
            right_x = end_x - ARROW_SIZE * math.cos(angle - math.pi / 6)
            right_y = end_y - ARROW_SIZE * math.sin(angle - math.pi / 6)
            
            # Dessiner la flèche (triangle)
            arcade.draw_triangle_filled(left_x, left_y, end_x, end_y, right_x, right_y, arcade.color.RED)
            

    def on_update(self, delta_time):
        """ Met à jour la logique du jeu """
        self.player_list.update()

        # Restreindre le joueur à l'intérieur des limites de la carte
        self.restrict_player_within_map()

        # Mettre à jour la caméra pour suivre le joueur
        self.center_camera_to_player()
        
        if len(self.items) < 3 and random.random() < 0.01:  # 5% chance d'ajouter un point à chaque frame
            print("APPEND ITEM")
            self.items.append(Item())

    def on_key_press(self, key, modifiers):
        """ Gérer les touches du clavier """
        if key == arcade.key.W or key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Gérer le relâchement des touches """
        if key in [arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN]:
            self.player_sprite.change_y = 0
        elif key in [arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT]:
            self.player_sprite.change_x = 0

    def restrict_player_within_map(self):
        """ Empêcher le joueur de sortir de la carte (image de fond) """
        # Limiter la position du joueur en fonction de la taille de la carte (image de fond)
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        if self.player_sprite.right > MAP_WIDTH:
            self.player_sprite.right = MAP_WIDTH
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        if self.player_sprite.top > MAP_HEIGHT:
            self.player_sprite.top = MAP_HEIGHT

    def center_camera_to_player(self):
        """ Centrer la caméra sur le joueur """
        # Déterminer le centre de la caméra en fonction de la position du joueur
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # Garder la caméra dans les limites de la carte
        screen_center_x = max(0, min(screen_center_x, MAP_WIDTH - SCREEN_WIDTH))
        screen_center_y = max(0, min(screen_center_y, MAP_HEIGHT - SCREEN_HEIGHT))

        # Appliquer la mise à jour de la position de la caméra
        self.camera.move_to((screen_center_x, screen_center_y), 0.1)

    def on_resize(self, width, height):
        """ Ajuster la caméra lorsque la fenêtre est redimensionnée """
        self.camera.resize(width, height)

# Lancer le jeu
if __name__ == "__main__":
    window = MyGame()
    arcade.run()
