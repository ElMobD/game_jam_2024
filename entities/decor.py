import arcade

class Decor(arcade.Sprite):
    def __init__(self, image_1, image_2, scale=1.0):
        # On initialise la classe Sprite avec la première image
        super().__init__(image_1, scale)
        
        # Sauvegarde les deux images
        self.image_1 = image_1
        self.image_2 = image_2
        
        # Position de l'objet
        self.center_x = 0
        self.center_y = 0

        # Variable d'état (1 ou 2) pour définir quelle image afficher
        self.state = 1

    # C'est pour afficher l'eau sur la carte
    def __init__(self, image, scale=1.0):
        # On initialise la classe Sprite avec l'image
        super().__init__(image, scale)
            
        # Sauvegarde l'image
        self.image_1 = image
        self.image_2 = None
            
        # Position de l'objet
        self.center_x = 90
        self.center_y = 810

        # Variable d'état (1) pour définir quelle image afficher
        self.state = 1

    def update_image(self):
        """ Change l'image en fonction de l'état """
        if self.state == 1:
            self.texture = arcade.load_texture(self.image_1)
        elif self.state == 2:
            self.texture = arcade.load_texture(self.image_2)

    def set_state(self, new_state):
        """ Modifie l'état et met à jour l'image """
        if new_state in [1, 2]:
            self.state = new_state
            self.update_image()