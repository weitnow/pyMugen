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
        self.key_map = {
            pygame.K_d: Action.MOVE_RIGHT,
            pygame.K_a: Action.MOVE_LEFT,
            pygame.K_s: Action.MOVE_DOWN,
            pygame.K_w: Action.MOVE_UP,
            pygame.K_z: Action.MOVE_A,
            pygame.K_u: Action.MOVE_B
        }

    def get_pressed_actions(self):
        keys = pygame.key.get_pressed()
        pressed_actions = set()
        for key, action in self.key_map.items():
            if keys[key]:
                pressed_actions.add(action)
        print(pressed_actions) #TODO: remove
        return pressed_actions


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
