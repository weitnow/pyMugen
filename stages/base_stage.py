from gameobjects.game_object import GameObject
from gameobjects.sprite import RenderAnchor
from managers.service_provider import ServiceProvider

class BaseStage():
    def __init__(self, world_pos):
        self._sp = ServiceProvider()
        self._vm = self._sp.view_manager
        self.camera = self._vm.camera

        self.stage_front = GameObject(world_pos, RenderAnchor.BOTTOMCENTER) #not affected by camera
        self.stage_back = GameObject(world_pos, RenderAnchor.BOTTOMCENTER)

        self.stage_width = 0 # will be set by the stage, but we initialize it to 0 here
        self.stage_height = 0 # will be set by the stage, but we initialize it to 0 here


    def update(self, dt):
        self.stage_front.update(dt)
        self.stage_back.update(dt)

    def draw(self):
        
        self.stage_front.draw() 
        self.stage_back.draw()

    def debug_draw(self):
        #self.stage_front.debug_draw() not affected by camera, so no need to debug draw
        self.stage_back.debug_draw()

    def configure_camera(self):
        self.camera.world_width = self.stage_width
        self.camera.world_height = self.stage_height
        self.camera.world_center_x = self.stage_center_x
        self.camera.world_center_y = self.stage_center_y