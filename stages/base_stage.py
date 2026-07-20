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

        self.allowed_camera_y_travel_min = 0 # how far the camera can move in y from the center of the stage, will be set by the stage based on world height and view height
        self.allowed_camera_y_travel_max = 0 # how far the camera can move in y from the center of the stage, will be set by the stage based on world height and view height

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
        self.camera.world_center_x = int(self.stage_front.world_pos.x) # anchor is bottomcenter, so we can use the x position of the stage front as the center of the stage
        self.camera.world_center_y = int(self.stage_front.world_pos.y - self.stage_height // 2) # anchor is bottomcenter, so we can use the y position of the stage front minus half the stage height as the center of the stage
        self.camera.x_travel = int((self.stage_width - self.camera.view_width) / 2)
        self.camera.y_travel_min = self.allowed_camera_y_travel_min
        self.camera.y_travel_max = self.allowed_camera_y_travel_max