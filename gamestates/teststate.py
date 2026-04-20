

from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import Action
from gameobjects.sprite import Sprite
from gameobjects.components.physics_components import FighterPhysicsComponent
from gameobjects.components.player_controller_component import PlayerController
import pygame

from gameobjects.sprite import RenderAnchor



class TestState(GameState):

    def enter(self):
        #create a game object and add sprite
        self.mySprite1 = Sprite().set_anim_name("debug32")
        self.mySprite1.set_frame(0)

        self.myGameObject = GameObject(world_pos=(128,32), render_anchor=RenderAnchor.CENTER)
        self.myGameObject.add_sprite(Sprite().set_anim_name("debug32").set_frame(1))
        self.myGameObject.add_camera(self.view_manager.camera)
        self.myGameObject.add_physics(FighterPhysicsComponent())
        self.myGameObject.specialmovelist = {
            "Fireball": [Action.DOWN, Action.DOWN_RIGHT, Action.RIGHT, Action.A],
            "Shoryuken": [Action.RIGHT, Action.DOWN, Action.DOWN_RIGHT, Action.A],
            "Sonic Boom": [Action.LEFT, Action.RIGHT, Action.A],
            "Super Kick": [Action.DOWN, Action.UP, Action.A],}
        self.myGameObject.add_player_controller(PlayerController(0, self.myGameObject))

        self.myStage = Sprite().set_anim_name("stages").set_frame(3)


 

    def exit(self):
        pass

    def handle_input(self):
        actions = self.input_manager.get_just_pressed_actions(0)
        actions_held = self.input_manager.get_pressed_actions(0)

        if Action.RIGHT in actions_held:
            self.myGameObject.physics.move_right()

        elif Action.LEFT in actions_held:
            self.myGameObject.physics.move_left()
        else:
            self.myGameObject.physics.stop()
 
        if Action.UP in actions:
            self.myGameObject.physics.move_up()

        if Action.DOWN in actions:
            pass

        
        #temp
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            self.view_manager.camera.x += 1
        elif keys[pygame.K_m]:
            self.view_manager.camera.x -= 1
        


    def update(self, dt):
        #self.view_manager.camera.update(self.player1, self.player2) # simple camera follow for testing, can be expanded later for more complex behavior (like lookahead, shake, etc)
        
        self.mySprite1.update(dt)

        self.myGameObject.update(dt)


        super().update(dt)

    



    def draw(self):
        self.myStage.draw(self.view_manager.game_surface, (0, 0), render_anchor=RenderAnchor.TOPLEFT, camera=self.view_manager.camera)

        self.mySprite1.draw(self.view_manager.game_surface, (32, 32), render_anchor=RenderAnchor.CENTER, camera=self.view_manager.camera)

        self.myGameObject.draw(self.view_manager.game_surface)
 

        super().draw()



    def debug_draw(self):
        self.mySprite1.debug_draw(self.view_manager.debug_surface, (32, 32), render_anchor=RenderAnchor.CENTER, camera=self.view_manager.camera)

        self.myGameObject.debug_draw(self.view_manager.debug_surface)
 
        super().debug_draw()

    

