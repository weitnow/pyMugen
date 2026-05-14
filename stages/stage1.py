from gameobjects.game_object import GameObject
from gameobjects.sprite import RenderAnchor
from stages.base_stage import BaseStage

class Stage1(BaseStage):
    def __init__(self, world_pos=(0, 60)):
        super().__init__(world_pos=world_pos)
        self.stage_front.set_anim_name("stage1-front").set_frame(0).set_scale(3).use_camera(False)
        self.stage_back.set_anim_name("stage1-back").set_frame(0).set_scale(3)
        self.stage_width = self.stage_front.sprites[0].image.get_width() * self.stage_front.scale
