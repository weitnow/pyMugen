import pygame
from enum import Enum, auto
from collections import deque

# --- Enums for actions and directions ---
class Action(Enum):
    MOVE_RIGHT = auto()
    MOVE_LEFT = auto()
    MOVE_DOWN = auto()
    JUMP = auto()
    PUNCH = auto()

class Special(Enum):
    FIREBALL = auto()

# --- Input Manager ---
class InputManager:
    def __init__(self):
        self.key_map = {
            pygame.K_RIGHT: Action.MOVE_RIGHT,
            pygame.K_LEFT: Action.MOVE_LEFT,
            pygame.K_DOWN: Action.MOVE_DOWN,
            pygame.K_SPACE: Action.JUMP,
            pygame.K_z: Action.PUNCH
        }

    def get_pressed_actions(self):
        keys = pygame.key.get_pressed()
        pressed_actions = set()
        for key, action in self.key_map.items():
            if keys[key]:
                pressed_actions.add(action)
        return pressed_actions

# --- Player Controller ---
class PlayerController:
    def __init__(self):
        # Current intentions
        self.actions = {action: False for action in Action}

        # Input buffer for special moves
        self.input_buffer = deque(maxlen=20)  # store last 20 frames of input
        self.specials = []

    def update(self, pressed_actions):
        # Reset intentions
        for action in self.actions:
            self.actions[action] = False

        # Update current intentions
        for action in pressed_actions:
            self.actions[action] = True

        # Add to buffer
        self.input_buffer.append(pressed_actions)

        # Check for specials
        self.check_specials()

    def check_specials(self):
        # Example: Down, Down-Forward, Forward + Punch = Fireball
        # We simplify directions to sets of pressed actions per frame

        # Need at least 4 frames in buffer to detect this move
        if len(self.input_buffer) < 4:
            return

        # Convert last 4 frames to a list for easy access
        last_inputs = list(self.input_buffer)[-4:]

        # Check for Fireball sequence
        sequence = [
            {Action.MOVE_DOWN},
            {Action.MOVE_DOWN, Action.MOVE_RIGHT},
            {Action.MOVE_RIGHT},
            {Action.PUNCH}
        ]

        match = all(seq.issubset(frame) for seq, frame in zip(sequence, last_inputs))
        if match:
            self.specials.append(Special.FIREBALL)
            print("FIREBALL EXECUTED!")

# --- Player Object ---
class Player:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.size = (30, 50)
        self.on_ground = True
        self.controller = PlayerController()

    def update(self, dt):
        actions = self.controller.actions

        speed = 200
        gravity = 2000
        jump_velocity = -600
        ground_y = 250

        # Horizontal movement
        if actions[Action.MOVE_RIGHT]:
            self.pos.x += speed * dt
        if actions[Action.MOVE_LEFT]:
            self.pos.x -= speed * dt

        # Jump
        if actions[Action.JUMP] and self.on_ground:
            self.vel.y = jump_velocity
            self.on_ground = False

        # Gravity
        self.vel.y += gravity * dt
        self.pos.y += self.vel.y * dt

        # Ground collision
        if self.pos.y >= ground_y:
            self.pos.y = ground_y
            self.vel.y = 0
            self.on_ground = True

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 50, 50), (*self.pos, *self.size))

# --- Main Loop ---
pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

player = Player((200, 250))
input_manager = InputManager()

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Update input ---
    pressed = input_manager.get_pressed_actions()
    player.controller.update(pressed)

    # --- Update player ---
    player.update(dt)

    # --- Draw ---
    screen.fill((30, 30, 30))
    player.draw(screen)
    pygame.display.flip()

pygame.quit()
