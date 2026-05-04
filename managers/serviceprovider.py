import pygame
from decorators import singleton


from managers.graphic_manager import GraphicManager
from managers.view_manager.view_manager import ViewManager
from managers.debug_manager import DebugManager
from managers.input_manager import InputManager
from managers.gamestate_manager import GameStateManager
from managers.sound_manager import SoundManager
from gamesettings.settings_manager import SettingsManager

@singleton
class ServiceProvider:
    def __init__(self):
        self.gamestate_manager = GameStateManager()
        self.input_manager = InputManager()
        self.debug_manager = DebugManager()
        self.graphic_manager = GraphicManager()
        self.sound_manager = SoundManager()
        self.settings_manager = SettingsManager()
        self.view_manager = ViewManager()