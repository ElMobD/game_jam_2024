import arcade
from core.game import MyGame

def main():
    # Lancer le jeu
    # window = MyGame()
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()