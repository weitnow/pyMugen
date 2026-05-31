from gameobjects.game_object import GameObject
from gameobjects.sprite import RenderAnchor
from stages.base_stage import BaseStage

class Stage1(BaseStage):
    def __init__(self, world_pos=(480, 470)): #(-120, 61)
        super().__init__(world_pos=world_pos)
        self.stage_front.set_anim_name("stage1-front").set_frame_tag("Idle").set_scale(3)
        self.stage_back.set_anim_name("stage1-back").set_frame_tag("Idle").set_scale(3).enable_camera()
        self.stage_width = self.stage_front.sprite_size[0]
        self.stage_height = self.stage_front.sprite_size[1]

        self.allowed_camera_y_travel_min = -18 # means down
        self.allowed_camera_y_travel_max = 16 # means up
    
        
        self.configure_camera()

