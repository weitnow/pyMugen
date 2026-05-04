from abc import ABC, abstractmethod

import pygame
from managers.input_manager import InputManager
from managers.gamestate_manager import GameStateManager
from managers.view_manager.view_manager import ViewManager
from managers.debug_manager import DebugManager
from managers.sound_manager import SoundManager
from managers.settings_manager.settings_manager import SettingsManager

from gameobjects.game_object import GameObject


class GameState(ABC): #ABC is Abstract Base Class
    """Base class for all game states."""

    def __init__(self):
        # --- Managers ---
        # all managers are singletons, so we use the instance directly

        self.gamestate_manager: GameStateManager = GameStateManager()
        self.input_manager: InputManager = InputManager()
        self.view_manager: ViewManager = ViewManager()
        self.debug_manager: DebugManager = DebugManager()
        self.sound_manager: SoundManager = SoundManager()
        self.settings_manager: SettingsManager = SettingsManager()

        # references for easier access
        self.camera = self.view_manager.camera # reference for easy access
        self.GAME_VIEW_HEIGHT = self.view_manager.GAME_VIEW_HEIGHT
        self.GAME_VIEW_WIDTH = self.view_manager.GAME_VIEW_WIDTH

        # --- Game Objects ---
        self.player1: GameObject = None
        self.player2: GameObject = None
        self.projectiles_p1 = []
        self.projectiles_p2 = []
        self.game_objects = []

        # --- Stage ---
        self.stage: GameObject = None

    @abstractmethod
    def enter(self):
        """Called when the state is entered."""
        pass
        
    @abstractmethod
    def exit(self):
        """Called when the state is exited."""
        pass

    @abstractmethod
    def handle_input(self):
        """Handle input for the state."""
        pass

    @abstractmethod
    def update(self, dt):
        """Update the state logic."""
        if self.player1:
            self.player1.update(dt)
        if self.player2:
            self.player2.update(dt)
        for projectile in self.projectiles_p1:
            projectile.update(dt)
        for projectile in self.projectiles_p2:
            projectile.update(dt)
        for game_object in self.game_objects:
            game_object.update(dt)
        if self.stage:
            self.stage.update(dt)

    @abstractmethod
    def draw(self):
        """Draw the state. """
        if self.stage:
            self.stage.draw()
        for projectile in self.projectiles_p1:
            projectile.draw()
        for projectile in self.projectiles_p2:
            projectile.draw()
        for game_object in self.game_objects:
            game_object.draw()
        if self.player1:
            self.player1.draw()
        if self.player2:
            self.player2.draw()
        

    def debug_draw(self):
        """Draw debug information."""
        if self.stage:
            self.stage.debug_draw()
        for projectile in self.projectiles_p1:
            projectile.debug_draw()
        for projectile in self.projectiles_p2:
            projectile.debug_draw()
        for game_object in self.game_objects:
            game_object.debug_draw()
        if self.player1:
            self.player1.debug_draw()
        if self.player2:
            self.player2.debug_draw()
        


    def add_game_object(self, game_object: GameObject):
        """Add a game object to the state."""
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object: GameObject):
        """Remove a game object from the state."""
        self.game_objects.remove(game_object)

    def to_scaled_pos(self, pos: pygame.Vector2, scale: int = 4):
        """transform unscaled to scaled position"""
        return (int(pos.x * scale), int(pos.y * scale))
