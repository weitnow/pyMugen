import time
from collections import deque
from typing import Optional, Set
from enum import Enum, auto
import pygame

# --- Actions ---
class Action(Enum):
    RIGHT = auto()
    LEFT = auto()
    DOWN = auto()
    UP = auto()
    A = auto()
    B = auto()
    X = auto()
    Y = auto()
    LB = auto()
    RB = auto()
    LT = auto()
    RT = auto()
    
    # Diagonals
    DOWN_RIGHT = auto()
    DOWN_LEFT = auto()
    UP_RIGHT = auto()
    UP_LEFT = auto()


# --- Input Manager (Singleton) ---
class InputManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InputManager, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        # Keyboard mappings for 2 players
        self.key_maps = [
            {  # Player 1
                pygame.K_d: Action.RIGHT,
                pygame.K_a: Action.LEFT,
                pygame.K_s: Action.DOWN,
                pygame.K_w: Action.UP,
                pygame.K_z: Action.A,
                pygame.K_u: Action.B,
                pygame.K_j: Action.X,
                pygame.K_i: Action.Y,
                pygame.K_q: Action.LB,
                pygame.K_e: Action.RB,
                pygame.K_1: Action.LT,
                pygame.K_2: Action.RT,
            },
            {  # Player 2
                pygame.K_RIGHT: Action.RIGHT,
                pygame.K_LEFT: Action.LEFT,
                pygame.K_DOWN: Action.DOWN,
                pygame.K_UP: Action.UP,
                pygame.K_KP1: Action.A,
                pygame.K_KP2: Action.B,
                pygame.K_KP3: Action.X,
                pygame.K_KP4: Action.Y,
                pygame.K_KP5: Action.LB,
                pygame.K_KP6: Action.RB,
                pygame.K_KP7: Action.LT,
                pygame.K_KP8: Action.RT,
            },
        ]

        # Controller setup
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        # Controller button mapping (Xbox layout)
        self.button_map = {
            0: Action.A,
            1: Action.B,
            2: Action.X,
            3: Action.Y,
            4: Action.LB,
            5: Action.RB,
        }

        # State storage per player
        self.pressed_actions = [set(), set()]
        self.prev_pressed_actions = [set(), set()]

    def update(self):
        """Call once per frame to update all player inputs."""
        for player_index in (0, 1):
            self.prev_pressed_actions[player_index] = self.pressed_actions[player_index].copy()
            self.pressed_actions[player_index] = self._get_pressed_actions_now(player_index)

    def _get_pressed_actions_now(self, player_index: int) -> set:
        """Get currently pressed actions for a player."""
        actions = set()

        # Keyboard
        keys = pygame.key.get_pressed()
        for key, action in self.key_maps[player_index].items():
            if keys[key]:
                actions.add(action)

        # Controller
        if player_index < len(self.joysticks):
            js = self.joysticks[player_index]

            # Buttons
            for btn_id, action in self.button_map.items():
                if js.get_button(btn_id):
                    actions.add(action)

            # Triggers
            lt = js.get_axis(2)
            rt = js.get_axis(5)
            if lt > 0.3:
                actions.add(Action.LT)
            if rt > 0.3:
                actions.add(Action.RT)

            # D-Pad
            hat_x, hat_y = js.get_hat(0)
            if hat_x == 1:
                actions.add(Action.RIGHT)
            elif hat_x == -1:
                actions.add(Action.LEFT)
            if hat_y == 1:
                actions.add(Action.UP)
            elif hat_y == -1:
                actions.add(Action.DOWN)

        return actions

    def get_pressed_actions(self, player_index: int) -> set:
        return self.pressed_actions[player_index]

    def get_just_pressed_actions(self, player_index: int) -> set:
        return self.pressed_actions[player_index] - self.prev_pressed_actions[player_index]


# --- PlayerController ---
class PlayerController:
    def __init__(self, player_index: int):
        self.player_index = player_index
        self.input_manager = InputManager()
        
        # Current frame actions
        self.actions: dict[Action, bool] = {action: False for action in Action}
        
        # Detected special
        self.special_executed: Optional[str] = None
        
        # Simple input buffer: stores only new inputs as they happen
        self._input_sequence: deque[tuple[float, Action]] = deque()
        self._buffer_time: float = 0.7
        
        # Track last input to avoid duplicates
        self._last_input: Optional[Action] = None

        # Diagonal mappings
        self.DIAGONALS = {
            frozenset({Action.DOWN, Action.RIGHT}): Action.DOWN_RIGHT,
            frozenset({Action.DOWN, Action.LEFT}): Action.DOWN_LEFT,
            frozenset({Action.UP, Action.RIGHT}): Action.UP_RIGHT,
            frozenset({Action.UP, Action.LEFT}): Action.UP_LEFT,
        }

        # Simplified special patterns - just a sequence of actions
        self.special_patterns = {
            "Fireball": [Action.DOWN, Action.DOWN_RIGHT, Action.RIGHT, Action.A],
            "Shoryuken": [Action.RIGHT, Action.DOWN, Action.DOWN_RIGHT, Action.A],
            "Sonic Boom": [Action.LEFT, Action.RIGHT, Action.A],
            "Super Kick": [Action.DOWN, Action.UP, Action.UP, Action.A],
        }

    def normalize_diagonals(self, actions: frozenset[Action]) -> frozenset[Action]:
        """Convert cardinal direction combinations into diagonal actions."""
        new_actions = set(actions)
        for combo, diagonal_action in self.DIAGONALS.items():
            if combo.issubset(actions):
                new_actions -= combo
                new_actions.add(diagonal_action)
        return frozenset(new_actions)

    def update(self):
        """Update controller state - call once per frame."""
        pressed_actions = self.input_manager.get_pressed_actions(self.player_index)
        current_time = time.time()

        # Normalize diagonals
        pressed_actions = self.normalize_diagonals(frozenset(pressed_actions))

        # Update current actions dict
        for action in Action:
            self.actions[action] = action in pressed_actions

        # Add new inputs to sequence (only when they change)
        for action in pressed_actions:
            if action != self._last_input:
                self._input_sequence.append((current_time, action))
                self._last_input = action
                break  # Only track one new input per frame
        
        # If nothing pressed, reset last input
        if not pressed_actions:
            self._last_input = None

        # Clean old inputs from buffer
        while self._input_sequence and current_time - self._input_sequence[0][0] > self._buffer_time:
            self._input_sequence.popleft()

        # Clear previous special
        self.special_executed = None

        # Check for special moves
        self.check_specials()

    def check_specials(self):
        """Check if any special move pattern matches the input sequence."""
        if len(self._input_sequence) < 2:
            return
        
        # Extract just the actions from the sequence
        sequence = [action for _, action in self._input_sequence]
        
        # Check each special pattern
        for name, pattern in self.special_patterns.items():
            pattern_len = len(pattern)
            
            # Check if the end of our sequence matches the pattern
            if len(sequence) >= pattern_len:
                if sequence[-pattern_len:] == pattern:
                    print(f"🎯 SPECIAL EXECUTED: {name}")
                    self.special_executed = name
                    # Clear buffer to prevent re-triggering
                    self._input_sequence.clear()
                    self._last_input = None
                    return  # Only one special per frame

    def is_action_pressed(self, action: Action) -> bool:
        """Check if an action is currently pressed."""
        return self.actions.get(action, False)

    def get_special_executed(self) -> Optional[str]:
        """Get the special executed this frame (if any)."""
        return self.special_executed