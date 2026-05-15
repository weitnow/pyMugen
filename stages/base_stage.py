from gameobjects.game_object import GameObject
from gameobjects.sprite import RenderAnchor
from managers.service_provider import ServiceProvider

class BaseStage():
    def __init__(self, world_pos):
        self._sp = ServiceProvider()
        self._vm = self._sp.view_manager

        self.stage_front = GameObject(world_pos, RenderAnchor.TOPLEFT)
        self.stage_back = GameObject(world_pos, RenderAnchor.TOPLEFT)

        self.view_left_bound = self._vm.VIEW_LEFT_BOUND
        self.view_right_bound = self._vm.VIEW_RIGHT_BOUND
        self.view_top_bound = self._vm.VIEW_TOP_BOUND
        self.view_bottom_bound = self._vm.VIEW_BOTTOM_BOUND
        self.view_width = self.view_right_bound - self.view_left_bound
        self.view_height = self.view_bottom_bound - self.view_top_bound        
        
        self.stage_width = 0
        self.stage_height = 0

        
        

    def update(self, dt):
        self.stage_front.update(dt)
        self.stage_back.update(dt)

    def draw(self):
        
        self.stage_front.draw() 
        self.stage_back.draw()

    def debug_draw(self):
        pass
        
        #self.stage_front.debug_draw()
        #self.stage_back.debug_draw()