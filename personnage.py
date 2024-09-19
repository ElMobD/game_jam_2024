# personnage.py

import arcade
from variables import PLAYER_MOVEMENT_SPEED, STARTING_LIVES

class Personnage(arcade.Sprite):
    def __init__(self):
        # Charger la première image (dos par défaut)
        super().__init__("images/character_zombie_back.png", scale=0.5)

        # Charger les images nécessaires
        self.image_back = "images/character_zombie_back.png"
        self.image_walk_0 = "images/character_zombie_walk0.png"
        self.image_walk_1 = "images/character_zombie_walk1.png"
        self.image_wide = "images/character_zombie_wide.png"
        
        # Pour gérer l'animation (alterner entre 1 et 2)
        self.frame = 0  # Suivi du frame pour alterner entre les deux images

        self.center_x = 400  # Position initiale
        self.center_y = 300
        self.change_x = 0
        self.change_y = 0
        self.lives = STARTING_LIVES  # Trois vies pour le personnage

    def update_animation(self, delta_time: float = 1/60):
        """ Met à jour l'animation en fonction de la direction et du mouvement """

        # Alterner entre les images de marche toutes les x frames pour animer
        self.frame += 1
        if self.frame % 15 == 0:  # Change d'image toutes les 15 frames
            if self.change_y > 0:  # Vers le haut (dos)
                self.texture = arcade.load_texture(self.image_back)
            elif self.change_y < 0:  # Vers le bas (avant)
                if self.frame % 30 == 0:
                    self.texture = arcade.load_texture(self.image_walk_0)
                else:
                    self.texture = arcade.load_texture(self.image_walk_1)
            elif self.change_x > 0:  # Marche vers la droite (inverser l'image)
                if self.frame % 30 == 0:
                    self.texture = arcade.load_texture(self.image_walk_0 )
                else:
                    self.texture = arcade.load_texture(self.image_walk_1)
            elif self.change_x < 0:  # Marche vers la gauche (image normale)
                if self.frame % 30 == 0:
                    self.texture = arcade.load_texture(self.image_walk_0,mirrored=True)
                else:
                    self.texture = arcade.load_texture(self.image_walk_1,mirrored=True)
        
        # Si le personnage ne bouge pas, afficher l'image frontale large
        if self.change_x == 0 and self.change_y == 0:
            self.texture = arcade.load_texture(self.image_wide)

    def update(self):
        """ Mettre à jour la position du personnage """
        self.center_x += self.change_x
        self.center_y += self.change_y

    def restrict_within_map(self, map_width, map_height):
        """ Empêcher le personnage de sortir de la carte """
        if self.left < 0:
            self.left = 0
        if self.right > map_width:
            self.right = map_width
        if self.bottom < 0:
            self.bottom = 0
        if self.top > map_height:
            self.top = map_height

    def display_lives(self, camera_x, camera_y):
        """ Afficher le nombre de vies en haut à droite avec des cœurs """
        
        # Charger l'image du cœur
        heart_texture = arcade.load_texture("images/life.png")

        # Afficher un cœur pour chaque vie
        for i in range(self.lives):
            # Positionner chaque cœur avec un petit décalage 
            heart_x = camera_x + 650 + (i * 20)
            heart_y = camera_y + 580
            arcade.draw_texture_rectangle(heart_x, heart_y, 32, 32, heart_texture)

    # Méthode de collision entre le personnage et un item
    def check_collision_with_item(self, item):
        """
        Vérifie s'il y a une collision entre le personnage et un item.

        La collision est basée sur la distance entre les centres du personnage et de l'item.
        Si la distance entre les deux est inférieure à la somme des rayons, alors une collision est détectée.
        
        Paramètres:
        - item: l'instance de la classe Item à tester

        Retour:
        - bool: True si une collision est détectée, sinon False
        """
        # Calculer la distance entre le personnage et l'item
        distance = ((self.center_x - item.center_x) ** 2 + (self.center_y - item.center_y) ** 2) ** 0.5

        # Somme des rayons du personnage et de l'item
        combined_radius = self.radius + item.radius

        # Vérifier si la distance est inférieure à la somme des rayons (collision)
        if distance < combined_radius:
            return True
        else:
            return False
