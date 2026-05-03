import pygame
from enum import Enum, auto
from decorators import singleton


# --- Actions ---
class Action(Enum):
    RIGHT = auto()
    LEFT = auto()
    DOWN = auto()
    UP = auto()
    A = auto()
    B = auto()
    START = auto()
    
    # Diagonals
    DOWN_RIGHT = auto()
    DOWN_LEFT = auto()
    UP_RIGHT = auto()
    UP_LEFT = auto()


# --- Input Manager  ---
@singleton
class InputManager:

    def __init__(self):
  
        # Keyboard mappings for 2 players
        self.key_maps = [
            {  # Player 1
                pygame.K_d: Action.RIGHT,
                pygame.K_a: Action.LEFT,
                pygame.K_s: Action.DOWN,
                pygame.K_w: Action.UP,
                pygame.K_z: Action.A,
                pygame.K_u: Action.B,
                pygame.K_RETURN: Action.START,
           
            },
            {  # Player 2
                pygame.K_RIGHT: Action.RIGHT,
                pygame.K_LEFT: Action.LEFT,
                pygame.K_DOWN: Action.DOWN,
                pygame.K_UP: Action.UP,
                pygame.K_KP1: Action.A,
                pygame.K_KP2: Action.B,
                pygame.K_KP_ENTER: Action.START,
        
            },
        ]

        # Controller setup
        pygame.joystick.init()
        self.joysticks = [
            pygame.joystick.Joystick(i)
            for i in range(pygame.joystick.get_count())
        ]

        # Controller button mapping (Xbox layout)
        self.button_map = {
            0: Action.A,
            1: Action.B,
            7: Action.START,
    
        }

        # State storage per player
        self._pressed_actions = [set(), set()]
        self._prev_pressed_actions = [set(), set()]

    def update(self, dt):
        for i in (0, 1):
            # Store previous state by copying current
            self._prev_pressed_actions[i] = self._pressed_actions[i].copy()
            # Update current state
            self._pressed_actions[i] = self._quering_pressed_actions(i)

    def get_pressed_actions(self, player_index: int) -> set:
        return self._pressed_actions[player_index]

    def get_just_pressed_actions(self, player_index: int) -> set:
        return self._pressed_actions[player_index] - self._prev_pressed_actions[player_index]

    def _quering_pressed_actions(self, player_index: int) -> set:
        actions = set()

        keys = pygame.key.get_pressed()
        for key, action in self.key_maps[player_index].items():
            if keys[key]:
                actions.add(action)

        if player_index < len(self.joysticks):
            js = self.joysticks[player_index]

            # Buttons
            for btn_id, action in self.button_map.items():
                if js.get_button(btn_id):
                    actions.add(action)

           

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

   

