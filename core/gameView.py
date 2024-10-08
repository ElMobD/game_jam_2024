# Library
import arcade
import random
import math
import time

# Classes
from entities.item import Item
from entities.personnage import Personnage
from core.camera import CameraHandler
from utils.variables import MAP_HEIGHT, MAP_WIDTH
from entities.door import Door
from entities.decor import Decor
from entities.plante import Plante
from core.checkpoint_manager import CheckpointManager       

DISTANCE_LIMIT_HELP = 300
ARROW_OFFSET = 100
ARROW_SIZE = 20
TIME_LIMIT = 10  # in seconds

class GameView(arcade.View):
    def __init__(self, window, map_id):
        super().__init__(window)
        self.map_id = map_id

        # Charger l'image de fond selon la map
        self.background = arcade.load_texture(f"resources/images/background_{self.map_id}.png")

        # Charger l'eau
        self.water = Decor("resources/images/water2.png")

        # Créer le personnage
        self.player = Personnage()

        # Créer une liste de sprites pour le joueur
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Gérer la caméra
        self.camera_handler = CameraHandler(self.window, self.player)

        # Liste des objets
        self.items = []
        
        # Timer variables
        self.start_time = time.time()  # Initialize start time
        self.time_remaining = TIME_LIMIT
        
        # Score
        self.keys_collected = 0

        # Game Over flag
        self.game_over = False
        

        self.door = Door(MAP_WIDTH - 300, MAP_HEIGHT - 100)

        # Liste des clés randoms affichées
        self.keys_generated = 0
        self.max_keys_generated = 3
        
        # Créer une liste de sprites pour les plantes
        self.plant_list = arcade.SpriteList()
        self.create_plants()

        # Gérer les checkpoints
        self.checkpoint_manager = CheckpointManager()
        

    def create_plants(self):
        for _ in range(50):  # Arbres
            tree = Plante("resources/images/tree/foliagePack_010.png", scale=0.3) 
            self.plant_list.append(tree)
        
        for _ in range(50):  # sapin
            sapin = Plante("resources/images/tree/foliagePack_011.png", scale=0.3)  # sapin
            self.plant_list.append(sapin)


    def on_draw(self):
        arcade.start_render()

        # Appliquer la caméra
        self.camera_handler.use_camera()

        # Dessiner le fond
        arcade.draw_lrwh_rectangle_textured(0, 0, MAP_WIDTH, MAP_HEIGHT, self.background)

        # Dessiner le joueur
        self.player_list.draw()

        # Dessiner la porte
        self.door.draw()

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
            self.add_new_item()

        # Vérifier si le joueur a ramassé un objet
        self.player.collision_with_item(self.items)

        # Supprimer les objets collectés
        self.items = [item for item in self.items if not item.is_collected]

        # Mettre à jour le timer
        self.update_timer(delta_time)
        
        # camera_x, camera_y = self.camera_handler.get_camera_position()
        
        if arcade.check_for_collision(self.player, self.door):
            if self.player.keys == 3:
                next_view = self.window.view_manager.create_new_view(map_id=self.map_id + 1)
                self.window.show_view(next_view)
            else:
                if self.player.change_x > 0:
                    self.player.right = self.door.left
                elif self.player.change_x < 0:
                    self.player.left = self.door.right
                elif self.player.change_y > 0:
                    self.player.top = self.door.bottom
                elif self.player.change_y < 0:
                    self.player.bottom = self.door.top


    def add_new_item(self):
        if self.keys_generated < self.max_keys_generated:
            self.items.append(Item())
            self.keys_generated += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        
        self.player.handle_key_press(key)

        if key == arcade.key.SPACE:  # Activation du checkpoint avec la touche Espace
            print("Checkpoint créé !")
            self.checkpoint_manager.create_checkpoint(self.player, self.items)

        elif key == arcade.key.E:  # Revenir au dernier checkpoint avec la touche "E"
            if self.checkpoint_manager.checkpoint is not None:
                print("Restauration du checkpoint !")  # Message de débogage
                self.checkpoint_manager.restore_checkpoint(self.player, self.items)
            else:
                print("Aucun checkpoint disponible.")  # Message de débogage si aucun checkpoint


    def on_key_release(self, key, modifiers):
        self.player.handle_key_release(key)

    def draw_arrow_to_item(self, item):
        distance_x = item.center_x - self.player.center_x
        distance_y = item.center_y - self.player.center_y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if distance > DISTANCE_LIMIT_HELP:
            angle = math.atan2(distance_y, distance_x)
            arrow_x = self.player.center_x + ARROW_OFFSET * math.cos(angle)
            arrow_y = self.player.center_y + ARROW_OFFSET * math.sin(angle)
            
            end_x = arrow_x
            end_y = arrow_y
            left_x = end_x - ARROW_SIZE * math.cos(angle + math.pi / 6)
            left_y = end_y - ARROW_SIZE * math.sin(angle + math.pi / 6)
            right_x = end_x - ARROW_SIZE * math.cos(angle - math.pi / 6)
            right_y = end_y - ARROW_SIZE * math.sin(angle - math.pi / 6)
            
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

