import pygame
import globals

class GameView:
    def __init__(self):
        self.base_width = globals.GAME_RES[0]
        self.base_height = globals.GAME_RES[1]
        self.debug_scale = globals.DEBUG_SCALE

        # create base surfaces
        self.game_surface = pygame.Surface((self.base_width, self.base_height))
        self.debug_surface = pygame.Surface(
            (self.base_width * self.debug_scale, self.base_height * self.debug_scale), 
            pygame.SRCALPHA
        )

        # create initial window
        self._apply_display_mode()

        # overlay
        self.overlay_image = pygame.image.load("Assets/Graphics/Aseprite/overlay.png").convert_alpha()
        self.overlay_screen_rect = pygame.Rect(*globals.OVERLAY_VIEWPORT)

    # --- Internal helper ---
    def _apply_display_mode(self):
        if globals.fullscreen_enabled:
            self.fullscreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            width, height = globals.available_resolutions[globals.current_resolution_index]
            self.fullscreen = pygame.display.set_mode((width, height))
        self.screen_rect = self.fullscreen.get_rect()
        pygame.display.set_caption(f"Game View - {'Fullscreen' if globals.fullscreen_enabled else f'{self.fullscreen.get_width()}x{self.fullscreen.get_height()}'}")

    # --- Toggle fullscreen/windowed ---
    def toggle_fullscreen(self):
        self.fullscreen_enabled = not self.fullscreen_enabled
        self._apply_display_mode()

    # --- Cycle through resolutions ---
    def cycle_resolution(self):
        if not self.fullscreen_enabled:
            self.current_resolution_index = (self.current_resolution_index + 1) % len(self.available_resolutions)
            self._apply_display_mode()

    # --- Convert GameView coordinates to DebugView ---
    def to_debug_coords(self, x: float, y: float):
        return x * self.debug_scale, y * self.debug_scale
    
    def clear(self):
        self.game_surface.fill((30, 30, 30))
        self.debug_surface.fill((0, 0, 0, 0))

    # --- Draw everything ---
    def draw_to_screen(self):
        window_w, window_h = self.fullscreen.get_size()

        # --- calculate rendering area depending on overlay ---
        if globals.show_overlay:
            ow, oh = self.overlay_image.get_size()
            overlay_scale = window_h / oh
            overlay_scaled_w = int(ow * overlay_scale)
            overlay_scaled_h = window_h
            overlay_x = (window_w - overlay_scaled_w) // 2

            overlay_scaled = pygame.transform.scale(self.overlay_image, (overlay_scaled_w, overlay_scaled_h))
            render_rect = pygame.Rect(
                overlay_x + int(self.overlay_screen_rect.x * overlay_scale),
                int(self.overlay_screen_rect.y * overlay_scale),
                int(self.overlay_screen_rect.w * overlay_scale),
                int(self.overlay_screen_rect.h * overlay_scale)
            )
        else:
            render_rect = pygame.Rect(0, 0, window_w, window_h)

        # --- scaling ---
        game_aspect = self.base_width / self.base_height
        target_aspect = render_rect.w / render_rect.h

        if target_aspect > game_aspect:
            scale = render_rect.h / self.base_height
            new_width = int(self.base_width * scale)
            new_height = render_rect.h
            offset_x = render_rect.x + (render_rect.w - new_width) // 2
            offset_y = render_rect.y
        else:
            scale = render_rect.w / self.base_width
            new_width = render_rect.w
            new_height = int(self.base_height * scale)
            offset_x = render_rect.x
            offset_y = render_rect.y + (render_rect.h - new_height) // 2

        # draw
        scaled_game = pygame.transform.scale(self.game_surface, (new_width, new_height))
        self.fullscreen.fill((0, 0, 0))
        self.fullscreen.blit(scaled_game, (offset_x, offset_y))

        if globals.debug_draw:
            debug_scaled = pygame.transform.scale(self.debug_surface, (new_width, new_height))
            debug_scaled.set_alpha(160)
            self.fullscreen.blit(debug_scaled, (offset_x, offset_y))

        if globals.show_overlay:
            self.fullscreen.blit(overlay_scaled, (overlay_x, 0))

        pygame.display.flip()
