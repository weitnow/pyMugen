from gameobjects.game_object import GameObject
from gameobjects.sprite import RenderAnchor

class BaseStage():
    def __init__(self, world_pos):
        self.stage_front = GameObject(world_pos, RenderAnchor.TOPLEFT)
        self.stage_back = GameObject(world_pos, RenderAnchor.TOPLEFT)

    def update(self, dt):
        pass

    def draw(self):
        
        self.stage_front.draw() 
        self.stage_back.draw()

    def debug_draw(self):
        pass
        
        #self.stage_front.debug_draw()
        #self.stage_back.debug_draw()