import time
from collections import deque
from dataclasses import dataclass
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

# --- InputStep dataclass ---
@dataclass
class InputStep:
    actions: Set[Action]
    min_duration: float = 0.0
    must_release: bool = False  # Simplified: just check if actions should be released


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

    def get_just_released_actions(self, player_index: int) -> set:
        return self.prev_pressed_actions[player_index] - self.pressed_actions[player_index]


# --- PlayerController ---
class PlayerController:
    def __init__(self, player_index: int):
        self.player_index = player_index
        self.input_manager = InputManager()
        
        # Current frame actions
        self.actions: dict[Action, bool] = {action: False for action in Action}
        
        # Detected specials (cleared each frame, consumer should check and clear)
        self.specials: list[str] = []
        
        # Input buffer: stores (timestamp, frozenset[Action]) for each frame
        self._input_buffer: deque[tuple[float, frozenset[Action]]] = deque()
        self._buffer_time: float = 1.5  # Max time to keep inputs

        # Diagonal mappings
        self.DIAGONALS = {
            frozenset({Action.DOWN, Action.RIGHT}): Action.DOWN_RIGHT,
            frozenset({Action.DOWN, Action.LEFT}): Action.DOWN_LEFT,
            frozenset({Action.UP, Action.RIGHT}): Action.UP_RIGHT,
            frozenset({Action.UP, Action.LEFT}): Action.UP_LEFT,
        }

        # Define special move patterns
        self.special_patterns = {
            "Fireball": {
                "pattern": [
                    InputStep(actions={Action.DOWN}),
                    InputStep(actions={Action.DOWN_RIGHT}),
                    InputStep(actions={Action.RIGHT}),
                    InputStep(actions={Action.A}),
                ],
                "max_time": 0.5
            },
            "Shoryuken": {
                "pattern": [
                    InputStep(actions={Action.RIGHT}),
                    InputStep(actions={Action.DOWN}),
                    InputStep(actions={Action.DOWN_RIGHT}),
                    InputStep(actions={Action.A}),
                ],
                "max_time": 0.5
            },
            "Hold A": {
                "pattern": [
                    InputStep(actions={Action.A}, min_duration=1.0),
                    InputStep(actions={Action.A}, must_release=True),
                ],
                "max_time": 4.0 
            },
            "Charge": {
                "pattern": [
                    InputStep(actions={Action.LEFT}, min_duration=1.0),
                    InputStep(actions={Action.RIGHT, Action.A}),
                ],
                "max_time": 4.0
            },
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

        # Always add to buffer (important for timing accuracy)
        self._input_buffer.append((current_time, pressed_actions))

        # Clean old inputs
        while self._input_buffer and current_time - self._input_buffer[0][0] > self._buffer_time:
            self._input_buffer.popleft()

        # Clear previous specials
        self.specials.clear()

        # Check for special moves
        self.check_specials()

    def check_specials(self):
        """Check if any special move pattern matches the input buffer."""
        for name, special_data in self.special_patterns.items():
            pattern = special_data["pattern"]
            max_time = special_data["max_time"]
            
            if self.match_pattern(pattern, max_time):
                print(f"🎯 SPECIAL EXECUTED: {name}")
                self.specials.append(name)
                # Clear buffer to prevent re-triggering
                self._input_buffer.clear()
                break  # Only one special per frame

    def match_pattern(self, pattern: list[InputStep], max_time: float) -> bool:
        """Check if the pattern matches the input buffer."""
        if not self._input_buffer:
            return False

        current_time = time.time()
        
        # Filter buffer to only include inputs within max_time window
        valid_buffer = [
            (t, actions) for t, actions in self._input_buffer
            if current_time - t <= max_time
        ]
        
        if not valid_buffer:
            return False

        step_index = 0
        step_start_time = None
        i = 0

        while i < len(valid_buffer) and step_index < len(pattern):
            timestamp, actions = valid_buffer[i]
            step = pattern[step_index]

            # Handle release step
            if step.must_release:
                # Check if the actions are NOT present (released)
                if all(action not in actions for action in step.actions):
                    step_index += 1
                    step_start_time = None
                i += 1
                continue

            # Handle normal hold/press step
            if step.actions.issubset(actions):
                # Actions are being held
                if step_start_time is None:
                    step_start_time = timestamp
                
                hold_duration = timestamp - step_start_time
                
                # Check if minimum duration is met
                if hold_duration >= step.min_duration:
                    # Move to next step
                    step_index += 1
                    step_start_time = None
            else:
                # Actions not present - reset if we haven't satisfied min_duration
                if step.min_duration > 0:
                    step_start_time = None

            i += 1

        # Check if we completed all steps
        if step_index == len(pattern):
            total_duration = valid_buffer[-1][0] - valid_buffer[0][0]
            return total_duration <= max_time

        return False

    def is_action_pressed(self, action: Action) -> bool:
        """Check if an action is currently pressed."""
        return self.actions.get(action, False)

    def get_special_executed(self) -> Optional[str]:
        """Get the first special executed this frame (if any)."""
        return self.specials[0] if self.specials else None