import arcade
from utils.variables import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from core.manager.viewManager import ViewManager

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(width=800, height=600, title="Mon Jeu")
        self.view_manager = ViewManager(self)

    def setup_game(self):
        """ Méthode pour démarrer le jeu """
        initial_view = self.view_manager.create_new_view(map_id=1)
        self.show_view(initial_view)