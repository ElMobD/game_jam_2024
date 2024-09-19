import arcade
from entities.personnage import Personnage
from entities.item import Item
import random
from utils.variables import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MAP_HEIGHT, MAP_WIDTH, PLAYER_MOVEMENT_SPEED
from core.camera import CameraHandler
import math
import time

DISTANCE_LIMIT_HELP = 300  # Tolérance pour l'affichage des flèches
ARROW_OFFSET = 100  # Décalage pour dessiner la flèche
ARROW_SIZE = 20  # Taille de la flèche
KEYS_REQUIRED = 3
TIME_LIMIT = 60  # in seconds

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

        # Timer variables
        self.start_time = time.time()  # Initialize start time
        self.time_remaining = TIME_LIMIT

        # Score
        self.keys_collected = 0

        # Game Over flag
        self.game_over = False
        

    def on_draw(self):
        """ Fonction d'affichage """
        arcade.start_render()

        # Appliquer la caméra
        self.camera_handler.use_camera()

        # Dessiner le fond
        arcade.draw_lrwh_rectangle_textured(0, 0, MAP_WIDTH, MAP_HEIGHT, self.background)

        # Dessiner le joueur
        self.player_list.draw()

        # Afficher les vies et les clés du joueur
        camera_x, camera_y = self.camera_handler.get_camera_position()
        self.player.display_lives(camera_x, camera_y)
        self.player.display_inventory(camera_x, camera_y)

        # Dessiner les objets
        for item in self.items:
            item.draw()

        # Dessiner les flèches si le joueur est trop éloigné des items
        for item in self.items:
            self.draw_arrow_to_item(item)
            
        # Afficher le timer
        self.display_timer()

        # Afficher le message de fin de jeu si le jeu est terminé
        if self.game_over:
            self.draw_game_over()

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

        # Vérifier si le joueur a ramassé un objet
        self.player.collision_with_item(self.items)

        # Supprimer les objets collectés
      #  self.items = [item for item in self.items if not item.is_collected]

       # Mettre à jour le timer
        self.update_timer(delta_time)

    def on_key_press(self, key, modifiers):
        """ Gérer les touches du clavier """
        self.player.handle_key_press(key)

    def on_key_release(self, key, modifiers):
        """ Gérer le relâchement des touches """
        self.player.handle_key_release(key)

    def draw_arrow_to_item(self, item):
        """Dessine une flèche pointant vers l'item si trop loin du joueur"""

        # Calculer la distance entre le joueur et l'item
        distance_x = item.center_x - self.player.center_x
        distance_y = item.center_y - self.player.center_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if distance > DISTANCE_LIMIT_HELP:
            # Calculer l'angle pour déterminer la direction
            angle = math.atan2(distance_y, distance_x)
            
            # Calculer les coordonnées pour dessiner la flèche
            arrow_x = self.player.center_x + ARROW_OFFSET * math.cos(angle)
            arrow_y = self.player.center_y + ARROW_OFFSET * math.sin(angle)
            
            # Calculer les coordonnées des points de la flèche
            end_x = arrow_x
            end_y = arrow_y
            left_x = end_x - ARROW_SIZE * math.cos(angle + math.pi / 6)
            left_y = end_y - ARROW_SIZE * math.sin(angle + math.pi / 6)
            right_x = end_x - ARROW_SIZE * math.cos(angle - math.pi / 6)
            right_y = end_y - ARROW_SIZE * math.sin(angle - math.pi / 6)
            
            # Dessiner la flèche (triangle)
            arcade.draw_triangle_filled(left_x, left_y, end_x, end_y, right_x, right_y, arcade.color.RED)
        
    def update_timer(self, delta_time):
        """Met à jour le timer et vérifie si le temps est écoulé"""
        if not self.game_over:
            self.time_remaining -= delta_time
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.game_over = True
                self.check_game_over()

    def display_timer(self):
        """ Affiche le timer à l'écran """
        camera_x, camera_y = self.camera_handler.get_camera_position()
        time_text = f"Temps restant: {int(self.time_remaining)}s"
        arcade.draw_text(time_text, camera_x, camera_y, arcade.color.WHITE, 20)
        

    def check_game_over(self):
        """ Vérifie si le joueur a gagné ou perdu """
        if self.keys_collected < KEYS_REQUIRED:
            print("Game Over! Vous n'avez pas collecté toutes les clés à temps.")
            draw_game_over(self)
        else:
            print("Félicitations! Vous avez collecté toutes les clés.")

    def draw_game_over(self):
        """ Dessine le message de fin de jeu """
        arcade.draw_text("Game Over!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.RED, 40, anchor_x="center", anchor_y="center")
        arcade.draw_text("Appuyez sur 'R' pour redémarrer", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60, arcade.color.WHITE, 20, anchor_x="center", anchor_y="center")
            