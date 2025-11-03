import pygame
from enum import Enum, auto
from collections import deque
import time

# --- Enums ---
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
            pygame.K_d: Action.MOVE_RIGHT,
            pygame.K_a: Action.MOVE_LEFT,
            pygame.K_s: Action.MOVE_DOWN,
            pygame.K_w: Action.JUMP,
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
        self.actions = {action: False for action in Action}
        self.input_buffer = deque()  # store tuples (timestamp, pressed_actions)
        self.specials = []

        self.buffer_time = 0.3  # 300 ms input buffer

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
        # Fireball: Down, Down-Forward, Forward + Punch
        # Simplified for 2D: Down, Down+Right, Right, Punch
        sequence = [
            {Action.MOVE_DOWN},
            {Action.MOVE_DOWN, Action.MOVE_RIGHT},
            {Action.MOVE_RIGHT},
            {Action.PUNCH}
        ]

        # Convert buffer to just actions
        buffer_actions = [actions for _, actions in self.input_buffer]

        # Try to match sequence in order
        seq_index = 0
        for actions in buffer_actions:
            if sequence[seq_index].issubset(actions):
                seq_index += 1
                if seq_index == len(sequence):
                    # Fireball detected
                    self.specials.append(Special.FIREBALL)
                    print("FIREBALL EXECUTED!")
                    # Clear buffer so it doesn't repeat immediately
                    self.input_buffer.clear()
                    break

# --- Player ---
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

    pressed = input_manager.get_pressed_actions()
    player.controller.update(pressed)
    player.update(dt)

    screen.fill((30, 30, 30))
    player.draw(screen)
    pygame.display.flip()

pygame.quit()
