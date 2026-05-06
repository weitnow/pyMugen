from gameobjects.game_object import GameObject
from gameobjects.sprite import RenderAnchor

class BaseStage(GameObject):
    def __init__(self):
        super().__init__((0, 80), RenderAnchor.TOPLEFT)
