from abc import ABC, abstractmethod

import pygame
from input_manager import InputManager
from gamestate_manager import GameStateManager
from view_manager import ViewManager
from debug_manager import DebugManager
from sound_manager import SoundManager
from gamesettings.settings_manager import SettingsManager
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

        # --- Game Objects ---
        self.player1: GameObject = None
        self.player2: GameObject = None
        self.projectiles_p1 = []
        self.projectiles_p2 = []
        self.game_objects = []

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

    @abstractmethod
    def draw(self):
        """Draw the state. """
        if self.player1:
            self.player1.draw(self.view_manager.game_surface)
        if self.player2:
            self.player2.draw(self.view_manager.game_surface)
        for projectile in self.projectiles_p1:
            projectile.draw(self.view_manager.game_surface)
        for projectile in self.projectiles_p2:
            projectile.draw(self.view_manager.game_surface)
        for game_object in self.game_objects:
            game_object.draw(self.view_manager.game_surface)

    def debug_draw(self):
        """Draw debug information."""
        if self.player1:
            self.player1.draw_debug(self.view_manager.game_surface)
        if self.player2:
            self.player2.draw_debug(self.view_manager.game_surface)
        for projectile in self.projectiles_p1:
            projectile.draw_debug(self.view_manager.game_surface)
        for projectile in self.projectiles_p2:
            projectile.draw_debug(self.view_manager.game_surface)
        for game_object in self.game_objects:
            game_object.draw_debug(self.view_manager.game_surface)


    def add_game_object(self, game_object: GameObject):
        """Add a game object to the state."""
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object: GameObject):
        """Remove a game object from the state."""
        self.game_objects.remove(game_object)

    def to_scaled_pos(self, pos: pygame.Vector2, scale: int = 4):
        """transform unscaled to scaled position"""
        return (int(pos.x * scale), int(pos.y * scale))
