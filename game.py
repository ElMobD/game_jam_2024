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


class Personnage:
    def __init__(self):
        """Initialisation du personnage avec 3 vies"""
        self.sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", scale=0.5)
        self.sprite.center_x = SCREEN_WIDTH // 2
        self.sprite.center_y = SCREEN_HEIGHT // 2
        self.vies = 3
        self.change_x = 0
        self.change_y = 0

    def dessiner(self):
        """Dessiner le personnage"""
        self.sprite.draw()
       

    def mettre_a_jour(self):
        """Mettre à jour la position du personnage"""
        self.sprite.change_x = self.change_x
        self.sprite.change_y = self.change_y
        self.sprite.update()

    def gerer_touches_appuyees(self, key):
        """Gérer les touches du clavier pour le déplacement"""
        if key == arcade.key.W or key == arcade.key.UP:
            self.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.change_x = PLAYER_MOVEMENT_SPEED

    def gerer_touches_relachees(self, key):
        """Arrêter le déplacement quand les touches sont relâchées"""
        if key in [arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN]:
            self.change_y = 0
        elif key in [arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT]:
            self.change_x = 0

    def restreindre_dans_la_carte(self):
        """Empêcher le personnage de sortir de la carte"""
        if self.sprite.left < 0:
            self.sprite.left = 0
        if self.sprite.right > MAP_WIDTH:
            self.sprite.right = MAP_WIDTH
        if self.sprite.bottom < 0:
            self.sprite.bottom = 0
        if self.sprite.top > MAP_HEIGHT:
            self.sprite.top = MAP_HEIGHT

    def perdre_vie(self):
        """Réduire le nombre de vies"""
        self.vies -= 1
        if self.vies <= 0:
            print("Le personnage a perdu toutes ses vies !")
            # Vous pouvez ajouter d'autres logiques, comme terminer le jeu ou réinitialiser la partie.


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Charger l'image de fond
        self.background = arcade.load_texture("test.png")
        
        # Créer le personnage
        self.personnage = Personnage()

        # Configurer la caméra
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_draw(self):
        """Fonction d'affichage"""
        arcade.start_render()

        # Appliquer la caméra
        self.camera.use()

        # Dessiner le fond
        arcade.draw_lrwh_rectangle_textured(0, 0, MAP_WIDTH, MAP_HEIGHT, self.background)
        
        # Dessiner le personnage
        self.personnage.dessiner()

        # Afficher le nombre de vies en suivant la camera
        arcade.draw_text(f"Vies: {self.personnage.vies}", self.camera.viewport_left + 100, self.camera.viewport_top - 300, arcade.color.WHITE, 20)

    def on_update(self, delta_time):
        """Met à jour la logique du jeu"""
        self.personnage.mettre_a_jour()

        # Restreindre le joueur à l'intérieur des limites de la carte
        self.personnage.restreindre_dans_la_carte()

        # Mettre à jour la caméra pour suivre le joueur
        self.center_camera_to_player()

    def on_key_press(self, key, modifiers):
        """Gérer les touches du clavier"""
        self.personnage.gerer_touches_appuyees(key)

    def on_key_release(self, key, modifiers):
        """Gérer le relâchement des touches"""
        self.personnage.gerer_touches_relachees(key)

    def center_camera_to_player(self):
        """Centrer la caméra sur le personnage"""
        screen_center_x = self.personnage.sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.personnage.sprite.center_y - (self.camera.viewport_height / 2)

        # Garder la caméra dans les limites de la carte
        screen_center_x = max(0, min(screen_center_x, MAP_WIDTH - SCREEN_WIDTH))
        screen_center_y = max(0, min(screen_center_y, MAP_HEIGHT - SCREEN_HEIGHT))

        # Appliquer la mise à jour de la position de la caméra
        self.camera.move_to((screen_center_x, screen_center_y), 0.1)

    def on_resize(self, width, height):
        """Ajuster la caméra lorsque la fenêtre est redimensionnée"""
        self.camera.resize(width, height)


# Lancer le jeu
if __name__ == "__main__":
    window = MyGame()
    arcade.run()
