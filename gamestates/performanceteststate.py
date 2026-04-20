

from gamestates.gamestate_base import GameState
from gameobjects.game_object import GameObject, HitboxType, HurtboxType
from input_manager import Action
from gameobjects.sprite import Sprite
from gameobjects.components.physics_components import FighterPhysicsComponent
from gameobjects.components.player_controller_component import PlayerController
import pygame

from gameobjects.sprite import RenderAnchor


class PerformanceTestState(GameState):

    def enter(self):
        self.myStage = Sprite().set_anim_name("stages").set_frame(3)
        self.mySprite1 = Sprite().set_anim_name("debug32").set_frame(0)

        # List to hold our 90 test objects
        self.test_objects = []
        
        # Grid settings for spawning
        rows = 9
        cols = 10
        spacing = 40

        for i in range(90):
            # Calculate grid position
            x = 64 + (i % cols) * spacing
            y = 64 + (i // cols) * spacing
            
            obj = GameObject(world_pos=(x, y), render_anchor=RenderAnchor.CENTER)
            obj.add_sprite(Sprite().set_anim_name("debug32").set_frame(1))
            obj.add_camera(self.view_manager.camera)
            obj.add_physics(FighterPhysicsComponent())

            obj.specialmovelist = {
                "Fireball": [Action.DOWN, Action.DOWN_RIGHT, Action.RIGHT, Action.A],
                "Shoryuken": [Action.RIGHT, Action.DOWN, Action.DOWN_RIGHT, Action.A],
                "Sonic Boom": [Action.LEFT, Action.RIGHT, Action.A],
                "Super Kick": [Action.DOWN, Action.UP, Action.A],}
            
            # Every object gets a controller assigned to player index 0
            obj.add_player_controller(PlayerController(0, obj))
            
            self.test_objects.append(obj)

    def exit(self):
        pass

    def handle_input(self):
        # We only need to fetch the input state once per frame
        actions = self.input_manager.get_just_pressed_actions(0)
        actions_held = self.input_manager.get_pressed_actions(0)

        # Apply input logic to all 90 objects
        for obj in self.test_objects:
            if Action.RIGHT in actions_held:
                obj.physics.move_right()
            elif Action.LEFT in actions_held:
                obj.physics.move_left()
            else:
                obj.physics.stop()
    
            if Action.UP in actions:
                obj.physics.move_up()

        # Camera controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            self.view_manager.camera.x += 1
        elif keys[pygame.K_m]:
            self.view_manager.camera.x -= 1

    def update(self, dt):
        self.mySprite1.update(dt)
        
        # Update all 90 objects
        for obj in self.test_objects:
            obj.update(dt)

        super().update(dt)

    def draw(self):
        self.myStage.draw(self.view_manager.game_surface, (0, 0), 
                         render_anchor=RenderAnchor.TOPLEFT, camera=self.view_manager.camera)
        
        self.mySprite1.draw(self.view_manager.game_surface, (32, 32), 
                           render_anchor=RenderAnchor.CENTER, camera=self.view_manager.camera)

        # Draw all 90 objects
        for obj in self.test_objects:
            obj.draw(self.view_manager.game_surface)

        super().draw()

    def debug_draw(self):
        self.mySprite1.debug_draw(self.view_manager.debug_surface, (32, 32), 
                                 render_anchor=RenderAnchor.CENTER, camera=self.view_manager.camera)

        for obj in self.test_objects:
            obj.debug_draw(self.view_manager.debug_surface)
 
        super().debug_draw()