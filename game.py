import arcade

# Dimensions de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Carte avec fond PNG et caméra"

# Taille du fond (3 fois la taille de la fenêtre visible)
MAP_WIDTH = SCREEN_WIDTH * 3
MAP_HEIGHT = SCREEN_HEIGHT * 3

# Vitesse du joueur
PLAYER_MOVEMENT_SPEED = 5

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

    def on_draw(self):
        """ Fonction d'affichage """
        arcade.start_render()

        # Appliquer la caméra
        self.camera.use()

        # Dessiner le fond (les coordonnées 0, 0 sont en bas à gauche)
        arcade.draw_lrwh_rectangle_textured(0, 0, MAP_WIDTH, MAP_HEIGHT, self.background)
        
        # Dessiner le joueur
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Met à jour la logique du jeu """
        self.player_list.update()

        # Restreindre le joueur à l'intérieur des limites de la carte
        self.restrict_player_within_map()

        # Mettre à jour la caméra pour suivre le joueur
        self.center_camera_to_player()

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
