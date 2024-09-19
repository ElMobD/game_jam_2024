import arcade
from entities.personnage import Personnage
from entities.item import Item
import random
from utils.variables import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MAP_HEIGHT, MAP_WIDTH, PLAYER_MOVEMENT_SPEED
from core.camera import CameraHandler

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Charger l'image de fond
        self.background = arcade.load_texture("resources/images/background.png")

        # Créer le personnage
        self.player = Personnage()

        # Créer une liste de sprites pour le joueur
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Gérer la caméra
        self.camera_handler = CameraHandler(self, self.player)

        # Liste des objets
        self.items = []

    def on_draw(self):
        """ Fonction d'affichage """
        arcade.start_render()

        # Appliquer la caméra
        self.camera_handler.use_camera()

        # Dessiner le fond
        arcade.draw_lrwh_rectangle_textured(0, 0, MAP_WIDTH, MAP_HEIGHT, self.background)

        # Dessiner le joueur
        self.player_list.draw()

        # Afficher les vies du joueur
        camera_x, camera_y = self.camera_handler.get_camera_position()
        self.player.display_lives(camera_x, camera_y)

        # Dessiner les objets
        for item in self.items:
            item.draw()

    def on_update(self, delta_time):
        """ Met à jour la logique du jeu """
        self.player_list.update()
        self.player.update_animation(delta_time)

        # Restriction du joueur dans la carte
        self.player.restrict_within_map(MAP_WIDTH, MAP_HEIGHT)

        # Mise à jour de la caméra pour suivre le joueur
        self.camera_handler.center_camera_to_player()

        # Ajouter des objets de façon aléatoire
        if len(self.items) < 3 and random.random() < 0.01:
            self.items.append(Item())

    def on_key_press(self, key, modifiers):
        """ Gérer les touches du clavier """
        self.player.handle_key_press(key)

    def on_key_release(self, key, modifiers):
        """ Gérer le relâchement des touches """
        self.player.handle_key_release(key)
