from gameobjects.game_object import GameObject
from gameobjects.sprite import RenderAnchor
from managers.service_provider import ServiceProvider

class BaseStage():
    def __init__(self, world_pos):
        self._sp = ServiceProvider()
        self._vm = self._sp.view_manager
        self.camera = self._vm.camera

        self.stage_front = GameObject(world_pos, RenderAnchor.TOPLEFT)
        self.stage_back = GameObject(world_pos, RenderAnchor.TOPLEFT)

        self.view_left_bound = self._vm.VIEW_LEFT_BOUND
        self.view_right_bound = self._vm.VIEW_RIGHT_BOUND
        self.view_top_bound = self._vm.VIEW_TOP_BOUND
        self.view_bottom_bound = self._vm.VIEW_BOTTOM_BOUND
        self.view_width = self._vm.VIEW_WIDTH
        self.view_height = self._vm.VIEW_HEIGHT
        
        self.stage_width = 0 # will be set by the stage, but we initialize it to 0 here
        self.stage_height = 0 # will be set by the stage, but we initialize it to 0 here


        
        

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

    def configure_camera(self):
        self.camera.world_width = self.stage_width
        self.camera.world_height = self.stage_height