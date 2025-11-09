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

    # Diagonal directions
    DOWN_RIGHT = auto()
    DOWN_LEFT = auto()
    UP_RIGHT = auto()
    UP_LEFT = auto()

# --- Specials ---
class Special(Enum):
    FIREBALL = auto()
    SHORYUKEN = auto()
    CHARGE = auto()
    HOLD_A = auto()

# --- InputStep dataclass ---
@dataclass
class InputStep:
    actions: Set[Action] = frozenset()       # Buttons/directions to hold
    min_duration: float = 0                  # Minimum hold time (seconds)
    max_duration: Optional[float] = None    # Optional maximum allowed time for this step
    release: bool = False                    # True if step requires actions to be released


# --- Input Manager ---
class InputManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InputManager, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        # --- Keyboard mappings for 2 players ---
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

        # --- Controller setup ---
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        # --- Controller button mapping (Xbox layout) ---
        # Button indices may differ per controller model!
        self.button_map = {
            0: Action.A,   # A
            1: Action.B,   # B
            2: Action.X,   # X
            3: Action.Y,   # Y
            4: Action.LB,  # LB
            5: Action.RB,  # RB
        }

        # --- Store pressed actions per player ---
        self.pressed_actions = [set(), set()]

    def get_pressed_actions(self, player_index: int):
        """Return the set of actions for a specific player (0 or 1)."""
        if player_index not in (0, 1):
            return set()

        actions = self.pressed_actions[player_index]
        actions.clear()

        # --- Keyboard input ---
        keys = pygame.key.get_pressed()
        for key, action in self.key_maps[player_index].items():
            if keys[key]:
                actions.add(action)

        # --- Controller input ---
        if player_index < len(self.joysticks):
            js = self.joysticks[player_index]

            # Buttons (A, B, X, Y, LB, RB)
            for btn_id, action in self.button_map.items():
                if js.get_button(btn_id):
                    actions.add(action)

            # Triggers (LT, RT) — analog inputs
            lt = js.get_axis(2)  # Left trigger axis
            rt = js.get_axis(5)  # Right trigger axis
            if lt > 0.5:
                actions.add(Action.LT)
            if rt > 0.5:
                actions.add(Action.RT)

            # D-Pad (Hat)
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

# --- PlayerController ---
class PlayerController:
    def __init__(self):
        # Current frame actions
        self.actions: dict[Action, bool] = {action: False for action in Action}
        # Detected specials
        self.specials: list[Special] = []
        # Input buffer: deque of (timestamp, frozenset[Action])
        self._input_buffer: deque[tuple[float, frozenset[Action]]] = deque()
        # How long to keep inputs in buffer
        self._buffer_time: float = 0.7

        # Diagonal mappings
        self.DIAGONALS = {
            frozenset({Action.DOWN, Action.RIGHT}): Action.DOWN_RIGHT,
            frozenset({Action.DOWN, Action.LEFT}): Action.DOWN_LEFT,
            frozenset({Action.UP, Action.RIGHT}): Action.UP_RIGHT,
            frozenset({Action.UP, Action.LEFT}): Action.UP_LEFT,
        }

        # --- Define patterns for specials ---
        self.specials_definitions = {
            Special.FIREBALL: (
                [
                    InputStep(actions={Action.DOWN}),
                    InputStep(actions={Action.DOWN_RIGHT}),
                    InputStep(actions={Action.RIGHT}),
                    InputStep(actions={Action.A}),
                ],
                0.7
            ),
            Special.SHORYUKEN: (
                [
                    InputStep(actions={Action.RIGHT}),
                    InputStep(actions={Action.DOWN}),
                    InputStep(actions={Action.DOWN_RIGHT}),
                    InputStep(actions={Action.A}),
                ],
                0.7
            ),
            Special.HOLD_A: (
                [
                    InputStep(actions={Action.A}, min_duration=2.0),
                    InputStep(actions={Action.A}, release=True, min_duration=0)
                ],
                5.0
            ),
            Special.CHARGE: (
                [
                    InputStep(actions={Action.LEFT}, min_duration=2.0),
                    InputStep(actions={Action.RIGHT, Action.A}, max_duration=0.3)
                ],
                2.5
            ),
        }

    # --- Normalize diagonals ---
    def normalize_diagonals(self, actions: frozenset[Action]) -> frozenset[Action]:
        new_actions = set(actions)
        for combo, diagonal_action in self.DIAGONALS.items():
            if combo.issubset(actions):
                new_actions -= combo
                new_actions.add(diagonal_action)
        return frozenset(new_actions)

    # --- Update per frame ---
    def update(self, pressed_actions: Set[Action]):
        current_time = time.time()

        # Update current actions dict
        for action in self.actions:
            self.actions[action] = False
        for action in pressed_actions:
            self.actions[action] = True

        # Only add to buffer if changed
        if not self._input_buffer or pressed_actions != self._input_buffer[-1][1]:
            self._input_buffer.append((current_time, frozenset(pressed_actions)))

        # Remove old inputs beyond buffer time
        while self._input_buffer and current_time - self._input_buffer[0][0] > self._buffer_time:
            self._input_buffer.popleft()

        # Check specials
        self.check_specials()

    # --- Check all specials ---
    def check_specials(self):
        for special, (pattern, max_total_time) in self.specials_definitions.items():
            if self.match_pattern(pattern, max_total_time):
                self.specials.append(special)
                print(f"🎯 {special.name} executed!")
                self._input_buffer.clear()  # Clear buffer after detection

    # --- Match pattern ---
    def match_pattern(self, pattern: list[InputStep], max_total_time: float) -> bool:
        if not self._input_buffer:
            return False

        buf_list = list(self._input_buffer)
        start_time = buf_list[0][0]
        pattern_index = 0
        step_start_time = None

        for t, actions in buf_list:
            normalized_actions = self.normalize_diagonals(actions)
            current_step = pattern[pattern_index]

            if current_step.release:
                step_matched = current_step.actions.isdisjoint(normalized_actions)
                if step_matched:
                    # Release step only needs one frame of release
                    pattern_index += 1
                    step_start_time = None
                    if pattern_index >= len(pattern):
                        if t - start_time <= max_total_time:
                            return True
                        else:
                            return False
                # Don't reset step_start_time for release steps
            else:
                step_matched = current_step.actions.issubset(normalized_actions)
                if step_matched:
                    if step_start_time is None:
                        step_start_time = t
                    # Check min_duration
                    if t - step_start_time >= current_step.min_duration:
                        pattern_index += 1
                        step_start_time = None
                        if pattern_index >= len(pattern):
                            if t - start_time <= max_total_time:
                                return True
                            else:
                                return False
                else:
                    # Reset step timer if broken
                    step_start_time = None

        return False
