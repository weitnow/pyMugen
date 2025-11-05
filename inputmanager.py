import pygame
from enum import Enum, auto
from collections import deque
import time

# --- Enums ---
class Action(Enum):
    MOVE_RIGHT = auto()
    MOVE_LEFT = auto()
    MOVE_DOWN = auto()
    MOVE_UP = auto()
    MOVE_A = auto()
    MOVE_B = auto()

class Special(Enum):
    FIREBALL = auto()
    SHORYUKEN = auto()

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
                pygame.K_d: Action.MOVE_RIGHT,
                pygame.K_a: Action.MOVE_LEFT,
                pygame.K_s: Action.MOVE_DOWN,
                pygame.K_w: Action.MOVE_UP,
                pygame.K_z: Action.MOVE_A,
                pygame.K_u: Action.MOVE_B,
            },
            {  # Player 2
                pygame.K_RIGHT: Action.MOVE_RIGHT,
                pygame.K_LEFT: Action.MOVE_LEFT,
                pygame.K_DOWN: Action.MOVE_DOWN,
                pygame.K_UP: Action.MOVE_UP,
                pygame.K_KP1: Action.MOVE_A,
                pygame.K_KP2: Action.MOVE_B,
            },
        ]

        # --- Controller setup ---
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
     

        # --- Controller button mapping (Xbox layout) ---
        self.button_map = {
            0: Action.MOVE_A,  # A
            1: Action.MOVE_B,  # B
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

            # Buttons
            for btn_id, action in self.button_map.items():
                if js.get_button(btn_id):
                    actions.add(action)

            # D-Pad (Hat)
            hat_x, hat_y = js.get_hat(0)
            if hat_x == 1:
                actions.add(Action.MOVE_RIGHT)
            elif hat_x == -1:
                actions.add(Action.MOVE_LEFT)
            if hat_y == 1:
                actions.add(Action.MOVE_UP)
            elif hat_y == -1:
                actions.add(Action.MOVE_DOWN)

        return actions


# --- Player Controller ---
class PlayerController:
    def __init__(self):
        self.actions = {action: False for action in Action}
        self.input_buffer = deque()  # store tuples (timestamp, pressed_actions)
        self.specials = []

        self.buffer_time = 0.6  # 600 ms input buffer

    def update(self, pressed_actions):
        current_time = time.time()

        # Reset intentions
        for action in self.actions:
            self.actions[action] = False
        for action in pressed_actions:
            self.actions[action] = True

        # Add to buffer
        self.input_buffer.append((current_time, pressed_actions))

        # Remove old inputs
        while self.input_buffer and current_time - self.input_buffer[0][0] > self.buffer_time:
            self.input_buffer.popleft()

        # Check for specials
        self.check_specials()

    def check_specials(self):
        # Fireball: ↓, ↓→, →, Punch
        fireball_seq = [
            {Action.MOVE_DOWN},
            {Action.MOVE_DOWN, Action.MOVE_RIGHT},
            {Action.MOVE_RIGHT},
            {Action.MOVE_A}
        ]

        # Shoryuken: →, ↓, ↓→, Punch
        shoryuken_seq = [
            {Action.MOVE_LEFT},
            {Action.MOVE_LEFT},
            {Action.MOVE_RIGHT},
            {Action.MOVE_RIGHT},
            {Action.MOVE_A}
        ]

        buffer_actions = [actions for _, actions in self.input_buffer]

        def match_sequence(sequence):
            seq_index = 0
            for actions in buffer_actions:
                if sequence[seq_index].issubset(actions):
                    seq_index += 1
                    if seq_index == len(sequence):
                        return True
            return False

        if match_sequence(fireball_seq):
            self.specials.append(Special.FIREBALL)
            print("🔥 FIREBALL EXECUTED!")
            self.input_buffer.clear()

        elif match_sequence(shoryuken_seq):
            self.specials.append(Special.SHORYUKEN)
            print("💥 SHORYUKEN EXECUTED!")
            self.input_buffer.clear()
