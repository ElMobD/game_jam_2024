import arcade
from core.gameView import GameView

class ViewManager:
    def __init__(self, window):
        self.window = window

    def create_new_view(self, map_id):
        # Génère une nouvelle GameView avec un identifiant de map
        return GameView(self.window, map_id)
