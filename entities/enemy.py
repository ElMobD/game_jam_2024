import arcade
import random
import math

from utils.variables import MAP_HEIGHT, MAP_WIDTH

class Enemy(arcade.Sprite):
    def __init__(self, player):
        super().__init__("resources/images/character_zombie_back.png", scale=1)
        self.image_back = "resources/images/character_zombie_back.png"
        self.image_walk_0 = "resources/images/character_zombie_walk0.png"
        self.image_walk_1 = "resources/images/character_zombie_walk1.png"
        self.image_wide = "resources/images/character_zombie_wide.png"
        
        self.frame = 0
        self.player = player
        self.center_x = random.randint(100, MAP_WIDTH - 100)
        self.center_y = random.randint(100, MAP_HEIGHT - 100)
        self.speed = 2.5

    def update_animation(self, delta_time: float = 1/60):
        """Mise à jour de l'animation de l'ennemi en fonction de ses mouvements"""
        self.frame += 1
        if self.frame % 15 == 0:  # Changer la texture toutes les 15 frames
            if self.change_y > 0:
                self.texture = arcade.load_texture(self.image_back)
            elif self.change_y < 0:
                if self.frame % 30 == 0:
                    self.texture = arcade.load_texture(self.image_walk_0)
                else:
                    self.texture = arcade.load_texture(self.image_walk_1)
            elif self.change_x > 0:
                if self.frame % 30 == 0:
                    self.texture = arcade.load_texture(self.image_walk_0)
                else:
                    self.texture = arcade.load_texture(self.image_walk_1)
            elif self.change_x < 0:
                if self.frame % 30 == 0:
                    self.texture = arcade.load_texture(self.image_walk_0, mirrored=True)
                else:
                    self.texture = arcade.load_texture(self.image_walk_1, mirrored=True)

        # Si l'ennemi ne bouge pas, on affiche l'image "wide" (statique)
        if self.change_x == 0 and self.change_y == 0:
            self.texture = arcade.load_texture(self.image_wide)

    def follow_player(self):
        """Faire en sorte que l'ennemi suive le personnage"""
        if self.player.center_x > self.center_x:
            self.change_x = self.speed
        elif self.player.center_x < self.center_x:
            self.change_x = -self.speed

        if self.player.center_y > self.center_y:
            self.change_y = self.speed
        elif self.player.center_y < self.center_y:
            self.change_y = -self.speed

    def attack(self):
        """Attaquer le personnage si proche"""
        distance = math.sqrt((self.center_x - self.player.center_x) ** 2 +
                             (self.center_y - self.player.center_y) ** 2)
        if distance < 50:  # Distance d'attaque
            # print("Attaque réussie !")
            self.player.lives -= 1  # Diminuer les vies du personnage

    def update(self):
        self.follow_player()
        self.attack()
        super().update()
