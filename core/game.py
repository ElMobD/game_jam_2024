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
TIME_LIMIT = 10  # in seconds

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

        if self.game_over:
            self.display_game_over_message(camera_x, camera_y)


    def on_update(self, delta_time):
        """ Met à jour la logique du jeu """

        if self.game_over:
            return


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

        camera_x, camera_y = self.camera_handler.get_camera_position()

       # Mettre à jour le timer
        self.update_timer(delta_time)



    def on_key_press(self, key, modifiers):
        if self.game_over:
            return

        """ Gérer les touches du clavier """
        self.player.handle_key_press(key)

    def on_key_release(self, key, modifiers):
        if self.game_over:
            return

        """ Gérer le relâchement des touches """
        self.player.handle_key_release(key)

    def draw_arrow_to_item(self, item):
        if self.game_over:
            return

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
        camera_x, camera_y = self.camera_handler.get_camera_position()
        if not self.game_over:
            self.time_remaining -= delta_time
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.game_over = True

    def display_timer(self):
        """Affiche le timer au centre en haut de l'écran avec un look vintage."""
        camera_x, camera_y = self.camera_handler.get_camera_position()
        
        # Afficher un fond pour le timer
        arcade.draw_rectangle_filled(camera_x + 400, camera_y + 570, 160, 50, arcade.color.DARK_GRAY)
        
        # Calculer le temps restant en secondes
        time_text = f"Temps: {int(self.time_remaining)}s"
        # Afficher le timer
        arcade.draw_text(time_text, camera_x + 350, camera_y + 555,
                         arcade.color.WHITE, 14, font_name="Kenney Future")

    def display_game_over_message(self, x, y):
        """Affiche le message de Game Over"""
        arcade.draw_text("Game Over!", x+250, y+250, arcade.color.RED, 40, font_name="Kenney Future")
        


    

  
            