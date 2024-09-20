import arcade
from core.game import MyGame
from core.menuView import MenuView

def main():
    # Lancer le jeu
    window = MyGame()
    menu_view = MenuView(window)
    window.show_view(menu_view)  # Affiche la vue du menu
    arcade.run()

if __name__ == "__main__":
    main()