class CheckpointManager:
    def __init__(self):
        self.checkpoint = None  # Un seul checkpoint à la fois

    def create_checkpoint(self, player, objects):
        """Crée un checkpoint en sauvegardant la position du joueur et l'état des objets sur la carte"""
        self.checkpoint = {
            'player_position': (player.center_x, player.center_y),
            'objects': []
        }
        
        # Sauvegarder l'état de chaque objet sur la carte
        for obj in objects:
            obj_state = {
                'type': type(obj).__name__,  # Sauvegarder le type d'objet (Bridge, Door, etc.)
                'x': obj.center_x,
                'y': obj.center_y,
                'state': obj.state
            }
            self.checkpoint['objects'].append(obj_state)


        

    def restore_checkpoint(self, player, objects):
        """Restaure le dernier checkpoint enregistré"""
        if self.checkpoint is None:
            print("Aucun checkpoint disponible.")
            return  # Aucun checkpoint à restaurer
        
        # Restaurer la position du joueur
        player.center_x, player.center_y = self.checkpoint['player_position']

        # Restaurer l'état des objets
        for i, obj in enumerate(objects):
            obj_data = self.checkpoint['objects'][i]
            obj.center_x = obj_data['x']
            obj.center_y = obj_data['y']
            obj.update_state(obj_data['state'])
