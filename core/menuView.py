import arcade

class MenuView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.background_image = arcade.load_texture("resources/images/chronoshift.png")

    def on_draw(self):
        arcade.start_render()
        
        # Dessiner l'image de fond
        arcade.draw_texture_rectangle(
            self.window.width // 2, self.window.height // 2,
            self.window.width, self.window.height,
            self.background_image
        )
        
        # Dessiner les textes
        # "JOUER"
        play_text_x = self.window.width // 2 - 150
        play_text_y = self.window.height // 2
        play_text_width = 200
        play_text_height = 40
        play_text_margin = 10
        
        # Fond du texte "JOUER"
        arcade.draw_lrtb_rectangle_filled(
            play_text_x - play_text_width // 2 - play_text_margin,
            play_text_x + play_text_width // 2 + play_text_margin,
            play_text_y + play_text_height // 2 + play_text_margin,
            play_text_y - play_text_height // 2 - play_text_margin,
            arcade.color.GREEN
        )
        # Texte "JOUER"
        arcade.draw_text(
            "JOUER",
            play_text_x,
            play_text_y,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
            anchor_y="center"
        )
        
        # "QUITTER"
        quit_text_x = self.window.width // 2 + 150
        quit_text_y = self.window.height // 2
        quit_text_width = 200
        quit_text_height = 40
        quit_text_margin = 10
        
        # Fond du texte "QUITTER"
        arcade.draw_lrtb_rectangle_filled(
            quit_text_x - quit_text_width // 2 - quit_text_margin,
            quit_text_x + quit_text_width // 2 + quit_text_margin,
            quit_text_y + quit_text_height // 2 + quit_text_margin,
            quit_text_y - quit_text_height // 2 - quit_text_margin,
            arcade.color.RED
        )
        # Texte "QUITTER"
        arcade.draw_text(
            "QUITTER",
            quit_text_x,
            quit_text_y,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
            anchor_y="center"
        )
        
        rules_text_x = self.window.width // 2
        rules_text_y = self.window.height // 2 - 100
        arcade.draw_text("Règles du jeu : Collectez 3 clés pour accéder au niveau supérieur", rules_text_x, rules_text_y, arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # Définir les positions et dimensions des boutons
        play_text_x = self.window.width // 2 - 150
        play_text_y = self.window.height // 2
        play_text_width = 200
        play_text_height = 40
        play_text_margin = 10
        
        quit_text_x = self.window.width // 2 + 150
        quit_text_y = self.window.height // 2
        quit_text_width = 200
        quit_text_height = 40
        quit_text_margin = 10

        # Vérifier si le clic est dans la zone "JOUER"
        if (play_text_x - play_text_width // 2 - play_text_margin < x < play_text_x + play_text_width // 2 + play_text_margin and
            play_text_y - play_text_height // 2 - play_text_margin < y < play_text_y + play_text_height // 2 + play_text_margin):
            # Démarrer le jeu
            self.window.setup_game()
        
        # Vérifier si le clic est dans la zone "QUITTER"
        if (quit_text_x - quit_text_width // 2 - quit_text_margin < x < quit_text_x + quit_text_width // 2 + quit_text_margin and
            quit_text_y - quit_text_height // 2 - quit_text_margin < y < quit_text_y + quit_text_height // 2 + quit_text_margin):
            arcade.close_window()
