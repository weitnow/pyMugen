from abc import ABC, abstractmethod
from input_manager import InputManager
from gamestate_manager import GameStateManager
from game_view import GameView
from debug_manager import DebugManager




class GameState(ABC): #ABC is Abstract Base Class
    """Base class for all game states."""

    def __init__(self):
        
        self.game_state_manager: GameStateManager = GameStateManager()
        self.input_manager: InputManager = InputManager()
        self.view: GameView = GameView()
        self.debug_manager: DebugManager = DebugManager()

    @abstractmethod
    def enter(self):
        """Called when the state is entered."""
        pass
        
    @abstractmethod
    def exit(self):
        """Called when the state is exited."""
        pass

    @abstractmethod
    def update(self, dt):
        """Update the state logic."""
        pass

    @abstractmethod
    def draw(self):
        """Draw the state. """
        pass

    def debug_draw(self):
        """Draw debug information."""
        pass
