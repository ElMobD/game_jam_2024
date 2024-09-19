# Library
import arcade
import random
import math

# Classes
from entities.item import Item
from entities.personnage import Personnage
from core.camera import CameraHandler
from utils.variables import MAP_HEIGHT, MAP_WIDTH
from entities.door import Door

DISTANCE_LIMIT_HELP = 300
ARROW_OFFSET = 100
ARROW_SIZE = 20

class GameView(arcade.View):
    def __init__(self, window, map_id):
        super().__init__(window)
        self.map_id = map_id

        # Charger l'image de fond selon la map
        self.background = arcade.load_texture(f"resources/images/background_{self.map_id}.png")

        # Créer le personnage
        self.player = Personnage()

        # Créer une liste de sprites pour le joueur
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Gérer la caméra
        self.camera_handler = CameraHandler(self.window, self.player)

        # Liste des objets
        self.items = []

        self.door = Door(MAP_WIDTH - 300, MAP_HEIGHT - 100)

        # Liste des clés randoms affichées
        self.keys_generated = 0
        self.max_keys_generated = 3

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

    def on_update(self, delta_time):
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
        
        # if arcade.check_for_collision(self.player, self.door) and self.player.keys == 3:
        #     next_view = self.window.view_manager.create_new_view(map_id=self.map_id + 1)
        #     self.window.show_view(next_view)
        
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
