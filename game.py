import arcade

# Dimensions de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Jeu du Serpent avec Caméra Suivante"

# Constantes pour le serpent 
MOVEMENT_SPEED = 5
SNAKE_WIDTH = 20
SNAKE_HEIGHT = 20

# Largeur des bords
BORDER_WIDTH = 10

class Snake(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = SNAKE_WIDTH
        self.height = SNAKE_HEIGHT
        self.color = arcade.color.GREEN
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.change_x = 0
        self.change_y = 0

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

class SnakeGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Crée une caméra pour suivre le serpent
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Fond bleu ciel
        arcade.set_background_color(arcade.color.SKY_BLUE)
        
        # Crée le serpent
        self.snake = Snake()

    def on_draw(self):
        arcade.start_render()

        # Applique la caméra avant de dessiner
        self.camera.use()

        # Dessine les bords
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, BORDER_WIDTH // 2, SCREEN_WIDTH, BORDER_WIDTH, arcade.color.BLACK)  # Bord haut
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT - BORDER_WIDTH // 2, SCREEN_WIDTH, BORDER_WIDTH, arcade.color.BLACK)  # Bord bas
        arcade.draw_rectangle_filled(BORDER_WIDTH // 2, SCREEN_HEIGHT // 2, BORDER_WIDTH, SCREEN_HEIGHT, arcade.color.BLACK)  # Bord gauche
        arcade.draw_rectangle_filled(SCREEN_WIDTH - BORDER_WIDTH // 2, SCREEN_HEIGHT // 2, BORDER_WIDTH, SCREEN_HEIGHT, arcade.color.BLACK)  # Bord droit

        # Dessine le serpent
        self.snake.draw()

    def on_update(self, delta_time):
        # Met à jour la position du serpent
        self.snake.update()

        # Déplace la caméra pour qu'elle suive le serpent
        self.center_camera_to_player()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.snake.change_y = MOVEMENT_SPEED
            self.snake.change_x = 0
        elif key == arcade.key.DOWN:
            self.snake.change_y = -MOVEMENT_SPEED
            self.snake.change_x = 0
        elif key == arcade.key.RIGHT:
            self.snake.change_x = MOVEMENT_SPEED
            self.snake.change_y = 0
        elif key == arcade.key.LEFT:
            self.snake.change_x = -MOVEMENT_SPEED
            self.snake.change_y = 0

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.snake.change_y = 0
        elif key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.snake.change_x = 0

    def center_camera_to_player(self):
        # Définit la position où la caméra doit se centrer (autour du serpent)
        screen_center_x = self.snake.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.snake.center_y - (self.camera.viewport_height / 2)

        # Crée un vecteur pour la position de la caméra
        camera_position = screen_center_x, screen_center_y

        # Déplace la caméra à cette position
        self.camera.move_to(camera_position)

def main():
    game = SnakeGame()
    arcade.run()

if __name__ == "__main__":
    main()
