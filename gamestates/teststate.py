

from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from gameobjects.base_fighter import BaseFighter
from managers.input_manager import Action
from gameobjects.sprite import Sprite
from gameobjects.components.physics_components import FighterPhysicsComponent
from gameobjects.components.player_controller_component import PlayerController
import pygame

from gameobjects.sprite import RenderAnchor
from stages.stage1 import Stage1




class TestState(GameState):

    def enter(self):
        self.stage = Stage1()
        self.stage.configure_camera()


        self.overlay = Sprite().set_anim_name("gbOverlay").set_scale(3).set_frame(1)
 


        self.player1 = BaseFighter(world_pos=(128, 228), player_index=0).set_anim_name("gbFighter").set_frame_tag("Idle").set_scale(3)
        self.player2 = BaseFighter(world_pos=(384, 228), player_index=1).set_anim_name("gbFighter").set_frame_tag("Idle").set_scale(3)



    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)
        actions_held = self.input_manager.get_pressed_actions(0)
        
        # temp
        cam = self.camera
        cam.follow_enabled = True

        if Action.RIGHT in actions_held:
            pass

        elif Action.LEFT in actions_held:
            pass
        else:
            pass
 
        if Action.UP in actions_held:
            pass
          

        if Action.DOWN in actions_held:
            pass
         
   
        #temp
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            self.view_manager.camera.x -= 1
        elif keys[pygame.K_m]:
            self.view_manager.camera.x += 1
        


    def update(self, dt):
        self.view_manager.camera.update(dt, self.player1, self.player2)
        super().update(dt)


    def draw(self):
        super().draw()

        self.overlay.draw((0, 0), RenderAnchor.TOPLEFT)

       


    def debug_draw(self):
        super().debug_draw()



    

