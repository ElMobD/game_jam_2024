import arcade

class CameraHandler:
    def __init__(self, window, player):
        self.camera = arcade.Camera(window.width, window.height)
        self.player = player
        self.window = window

    def use_camera(self):
        """Appliquer la caméra"""
        self.camera.use()

    def center_camera_to_player(self):
        """Centrer la caméra sur le joueur"""
        screen_center_x = self.player.center_x - (self.window.width / 2)
        screen_center_y = self.player.center_y - (self.window.height / 2)

        screen_center_x = max(0, min(screen_center_x, self.window.width * 3 - self.window.width))
        screen_center_y = max(0, min(screen_center_y, self.window.height * 3 - self.window.height))

        self.camera.move_to((screen_center_x, screen_center_y), 0.1)

    def get_camera_position(self):
        """Retourne la position actuelle de la caméra"""
        return self.camera.position
