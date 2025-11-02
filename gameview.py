import pygame


class GameView:
    def __init__(self, base_width=256, base_height=144, debug_scale=8):
        self.base_width = base_width
        self.base_height = base_height
        self.debug_scale = debug_scale

        self.game_surface = pygame.Surface((base_width, base_height))
        self.debug_surface = pygame.Surface((base_width * debug_scale, base_height * debug_scale), pygame.SRCALPHA)
        self.fullscreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.fullscreen.get_rect()

        self.debug_draw = False

    # --- Convert GameView coordinates to DebugView ---
    def to_debug_coords(self, x: float, y: float):
        return x * self.debug_scale, y * self.debug_scale

    # --- Draw GameView to fullscreen with aspect ratio ---
    def draw_to_screen(self):
        window_w, window_h = self.fullscreen.get_size()
        game_aspect = self.base_width / self.base_height
        window_aspect = window_w / window_h

        if window_aspect > game_aspect:
            # window wider → pillarbox
            scale = window_h / self.base_height
            new_width = int(self.base_width * scale)
            new_height = window_h
            offset_x = (window_w - new_width) // 2
            offset_y = 0
        else:
            # window taller → letterbox
            scale = window_w / self.base_width
            new_width = window_w
            new_height = int(self.base_height * scale)
            offset_x = 0
            offset_y = (window_h - new_height) // 2

        # scale game view
        scaled = pygame.transform.scale(self.game_surface, (new_width, new_height))
        self.fullscreen.fill((0, 0, 0))
        self.fullscreen.blit(scaled, (offset_x, offset_y))

        # draw debug overlay if enabled
        if self.debug_draw:
            debug_scaled = pygame.transform.scale(self.debug_surface, (new_width, new_height))
            debug_scaled.set_alpha(160)
            self.fullscreen.blit(debug_scaled, (offset_x, offset_y))

        pygame.display.flip()

    def clear(self):
        self.game_surface.fill((30, 30, 30))
        self.debug_surface.fill((0, 0, 0, 0))
