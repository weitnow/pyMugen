from gameobject import GameObject

class Fighter(GameObject):
    def __init__(self, pos: tuple[float, float]):
        super().__init__(pos, rotatable=True)
        self.origin_center_bottom = True