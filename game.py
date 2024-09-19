# game.py

import arcade
from personnage import Personnage
from item import Item
import random
from variables import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MAP_HEIGHT, MAP_WIDTH, PLAYER_MOVEMENT_SPEED

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Charger l'image de fond
        self.background = arcade.load_texture("test.png")
        
        # Créer le personnage
        self.player = Personnage()

        # Créer une liste de sprites pour le joueur
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

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

        # Obtenir la position actuelle de la caméra
        camera_x, camera_y = self.camera.position

        # Afficher les vies en fonction de la position de la caméra
        self.player.display_lives(camera_x, camera_y)

        # Dessiner les objets
        for item in self.items:
            item.draw()

    def on_update(self, delta_time):
        """ Met à jour la logique du jeu """
        self.player_list.update()
        self.player.update_animation(delta_time)

        # Restreindre le joueur à l'intérieur des limites de la carte
        self.player.restrict_within_map(MAP_WIDTH, MAP_HEIGHT)

        # Mettre à jour la caméra pour suivre le joueur
        self.center_camera_to_player()
        
        if len(self.items) < 3 and random.random() < 0.01:  # 5% chance d'ajouter un point à chaque frame
            self.items.append(Item())

    def on_key_press(self, key, modifiers):
        """ Gérer les touches du clavier """
        if key == arcade.key.W or key == arcade.key.UP:
            self.player.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Gérer le relâchement des touches """
        if key in [arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN]:
            self.player.change_y = 0
        elif key in [arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0

    def center_camera_to_player(self):
        """ Centrer la caméra sur le joueur """
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        screen_center_x = max(0, min(screen_center_x, MAP_WIDTH - SCREEN_WIDTH))
        screen_center_y = max(0, min(screen_center_y, MAP_HEIGHT - SCREEN_HEIGHT))

        self.camera.move_to((screen_center_x, screen_center_y), 0.1)

    def on_resize(self, width, height):
        """ Ajuster la caméra lorsque la fenêtre est redimensionnée """
        self.camera.resize(width, height)

# Lancer le jeu
if __name__ == "__main__":
    window = MyGame()
    arcade.run()
