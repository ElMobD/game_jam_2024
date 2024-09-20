import arcade
from utils.variables import PLAYER_MOVEMENT_SPEED, STARTING_LIVES

class Personnage(arcade.Sprite):
    def __init__(self):
        super().__init__("resources/images/character_zombie_back.png", scale=1)
        self.image_back = "resources/images/character_zombie_back.png"
        self.image_walk_0 = "resources/images/character_zombie_walk0.png"
        self.image_walk_1 = "resources/images/character_zombie_walk1.png"
        self.image_wide = "resources/images/character_zombie_wide.png"
        
        self.frame = 0
        self.center_x = 200
        self.center_y = 200
        self.change_x = 0
        self.change_y = 0
        self.lives = STARTING_LIVES
        
        # inventaire de clés
        self.keys = 0
        # Liste des plantes
        self.plant_list = arcade.SpriteList()

    def update_animation(self, delta_time: float = 1/60):
        """ Mise à jour de l'animation """
        self.frame += 1
        if self.frame % 15 == 0:
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
        if self.change_x == 0 and self.change_y == 0:
            self.texture = arcade.load_texture(self.image_wide)

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

    def display_inventory(self, camera_x, camera_y):
        """Afficher les clés récoltées en haut à gauche """
        # Afficher un fond pour le HUD
        arcade.draw_rectangle_filled(camera_x + 80, camera_y + 570, 160, 50, arcade.color.DARK_GRAY)


        # Afficher le nombre de clés récoltées en texte pixellisé
        arcade.draw_text(f"Clés : {self.keys}", camera_x + 50, camera_y + 555,
                         arcade.color.WHITE, 14, font_name="Kenney Future")

    def display_lives(self, camera_x, camera_y):
        """Afficher les vies du joueur en haut à droite."""
        # Afficher un fond pour les vies
        arcade.draw_rectangle_filled(camera_x + 720, camera_y + 570, 160, 50, arcade.color.DARK_GRAY)

        # Afficher le nombre de vies sous forme de texte
        arcade.draw_text(f"Vies : {self.lives}", camera_x + 670, camera_y + 555,arcade.color.WHITE, 14, font_name="Kenney Future")

    def handle_key_press(self, key):
        """ Gérer les touches du clavier """
        if key == arcade.key.W or key == arcade.key.UP:
            self.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.change_x = PLAYER_MOVEMENT_SPEED

    def handle_key_release(self, key):
        """ Gérer le relâchement des touches """
        if key in [arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN]:
            self.change_y = 0
        elif key in [arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT]:
            self.change_x = 0


    def collision_with_item(self, items):
        # Parcourir tous les objets sur la map
        for item in items:
            # Vérifier si le personnage entre en collision avec l'objet
            if not item.is_collected and arcade.check_for_collision(self, item):
                # Ajouter l'objet à l'inventaire
                self.keys += 1
                print(f"Nombre de clés: {self.keys}")  # Debug: afficher le nombre de clés collectées
                # Supprimer l'objet de la carte (le marquer comme collecté)
                item.delete()
                

  