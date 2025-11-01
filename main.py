import pygame
from ressourcemanager import ResourceManager
from gameobject import GameObject

# --- Configuration ---
GAME_RES = (256, 144)
DEBUG_SCALE = 6
DEBUG_RES = (GAME_RES[0] * DEBUG_SCALE, GAME_RES[1] * DEBUG_SCALE)
DEBUG_DRAW = True  # toggle for debug overlay

# --- Initialize ---
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_info = pygame.display.Info()
SCREEN_RES = (display_info.current_w, display_info.current_h)
clock = pygame.time.Clock()

# --- Game & Debug canvases ---
game_surface = pygame.Surface(GAME_RES)
debug_surface = pygame.Surface(DEBUG_RES, pygame.SRCALPHA)  # supports transparency

# --- Load resources ---
resources = ResourceManager()
resources.load_spritesheet("gbFighter", "Assets/Graphics/Aseprite/gbFighter.png", "Assets/Graphics/Aseprite/gbFighter.json")
resources.load_spritesheet("nesFighter", "Assets/Graphics/Aseprite/nesFighter.png", "Assets/Graphics/Aseprite/nesFighter.json")

# --- Create objects ---
player = GameObject((100, 100))
player.get_anim("gbFighter")
player.get_anim("nesFighter")
player.set_anim("nesFighter")
player.set_frame_tag("Idle")

enemy = GameObject((150, 100))
enemy.get_anim("gbFighter")
enemy.set_anim("gbFighter")
enemy.set_frame_tag("Idle")

# --- Coordinate conversion helpers ---
def game_to_debug(x, y):
    """Convert gameview coordinates to debugview coordinates"""
    return int(x * DEBUG_SCALE), int(y * DEBUG_SCALE)

def draw_hitbox_debug(obj):
    """Example: draw a hitbox and hurtbox in debug view"""
    if not hasattr(obj, "rect"):
        return
    hx, hy = game_to_debug(obj.rect.x, obj.rect.y)
    hw, hh = obj.rect.width * DEBUG_SCALE, obj.rect.height * DEBUG_SCALE

    # Draw hurtbox (blue)
    pygame.draw.rect(debug_surface, (0, 0, 255, 80), (hx, hy, hw, hh), 2)

    # Example hitbox (red)
    # In a real system you'd use obj.hitbox etc.
    pygame.draw.rect(debug_surface, (255, 0, 0, 80), (hx + 8, hy, hw - 16, hh), 2)

# --- Aspect ratio scaler ---
def blit_scaled_center(source, target):
    """Scale source surface to fit target while keeping aspect ratio and black bars"""
    sw, sh = source.get_size()
    tw, th = target.get_size()

    scale = min(tw / sw, th / sh)
    new_size = (int(sw * scale), int(sh * scale))
    scaled = pygame.transform.scale(source, new_size)

    x = (tw - new_size[0]) // 2
    y = (th - new_size[1]) // 2

    target.fill((0, 0, 0))
    target.blit(scaled, (x, y))

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # --- Update ---
    player.update(dt)
    enemy.update(dt)

    # --- Draw gameview ---
    game_surface.fill((30, 30, 30))
    player.draw(game_surface)
    enemy.draw(game_surface)

    # --- Draw debugview ---
    debug_surface.fill((0, 0, 0, 0))  # clear transparent
    if DEBUG_DRAW:
        draw_hitbox_debug(player)
        draw_hitbox_debug(enemy)

    # --- Combine ---
    blit_scaled_center(game_surface, screen)

    if DEBUG_DRAW:
        scaled_debug = pygame.transform.scale(debug_surface, screen.get_size())
        scaled_debug.set_alpha(128)
        screen.blit(scaled_debug, (0, 0))

    pygame.display.flip()

pygame.quit()
