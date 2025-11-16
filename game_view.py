import pygame
import globals
from decorators import singleton

@singleton
class GameView:
    def __init__(self):
        self.base_width = globals.GAME_RES[0]
        self.base_height = globals.GAME_RES[1]
        self.debug_scale = globals.DEBUG_SCALE
        
        # Pre-calculate aspect ratio
        self.game_aspect = self.base_width / self.base_height

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
        
        # Cache for scaled surfaces and calculations
        self._cached_overlay_scaled = None
        self._cached_dimensions = None  # (new_width, new_height)
        self._offset = None  # (offset_x, offset_y)
        self._overlay_x = 0
        self._last_window_size = None
        self._last_overlay_state = None
        
        # Reusable rect to avoid recreating
        self.render_rect = pygame.Rect(0, 0, 0, 0)

    # --- Internal helper ---
    def _apply_display_mode(self):
        if globals.fullscreen_enabled:
            self.fullscreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            width, height = globals.available_resolutions[globals.current_resolution_index]
            self.fullscreen = pygame.display.set_mode((width, height))
        self.screen_rect = self.fullscreen.get_rect()
        pygame.display.set_caption(f"Game View - {'Fullscreen' if globals.fullscreen_enabled else f'{self.fullscreen.get_width()}x{self.fullscreen.get_height()}'}")
        
        # Invalidate cache on mode change
        self._last_window_size = None
        self._cached_dimensions = None

    # --- Toggle fullscreen/windowed ---
    def toggle_fullscreen(self):
        globals.fullscreen_enabled = not globals.fullscreen_enabled
        self._apply_display_mode()

    # --- Cycle through resolutions ---
    def cycle_resolution(self):
        if not globals.fullscreen_enabled:
            globals.current_resolution_index = (globals.current_resolution_index + 1) % len(globals.available_resolutions)
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
        current_window_size = (window_w, window_h)
        current_overlay_state = globals.show_overlay
        
        # Check if we need to recalculate scaling/positioning
        needs_recalc = (
            self._last_window_size != current_window_size or
            self._last_overlay_state != current_overlay_state
        )
        
        if needs_recalc:
            self._last_window_size = current_window_size
            self._last_overlay_state = current_overlay_state
            
            # --- calculate rendering area depending on overlay ---
            if globals.show_overlay:
                ow, oh = self.overlay_image.get_size()
                overlay_scale = window_h / oh
                overlay_scaled_w = int(ow * overlay_scale)
                overlay_scaled_h = window_h
                self._overlay_x = (window_w - overlay_scaled_w) // 2
                
                # Cache overlay scaling (only recalculate when window size changes)
                self._cached_overlay_scaled = pygame.transform.scale(
                    self.overlay_image, 
                    (overlay_scaled_w, overlay_scaled_h)
                )
                
                self.render_rect.update(
                    self._overlay_x + int(self.overlay_screen_rect.x * overlay_scale),
                    int(self.overlay_screen_rect.y * overlay_scale),
                    int(self.overlay_screen_rect.w * overlay_scale),
                    int(self.overlay_screen_rect.h * overlay_scale)
                )
            else:
                self.render_rect.update(0, 0, window_w, window_h)

            # --- scaling calculations ---
            target_aspect = self.render_rect.w / self.render_rect.h

            if target_aspect > self.game_aspect:
                scale = self.render_rect.h / self.base_height
                new_width = int(self.base_width * scale)
                new_height = self.render_rect.h
                offset_x = self.render_rect.x + (self.render_rect.w - new_width) // 2
                offset_y = self.render_rect.y
            else:
                scale = self.render_rect.w / self.base_width
                new_width = self.render_rect.w
                new_height = int(self.base_height * scale)
                offset_x = self.render_rect.x
                offset_y = self.render_rect.y + (self.render_rect.h - new_height) // 2
            
            # Cache dimensions and offsets
            self._cached_dimensions = (new_width, new_height)
            self._offset = (offset_x, offset_y)
        
        # Use cached values
        new_width, new_height = self._cached_dimensions
        offset_x, offset_y = self._offset
        
        # Scale game surface (content changes every frame)
        scaled_game = pygame.transform.scale(self.game_surface, (new_width, new_height))
        
        # Draw
        self.fullscreen.fill((0, 0, 0))
        self.fullscreen.blit(scaled_game, (offset_x, offset_y))

        if globals.debug_draw:
            # Scale debug surface (content changes when debug is active)
            debug_scaled = pygame.transform.scale(self.debug_surface, (new_width, new_height))
            debug_scaled.set_alpha(160)
            self.fullscreen.blit(debug_scaled, (offset_x, offset_y))

        if globals.show_overlay:
            # Use cached scaled overlay
            self.fullscreen.blit(self._cached_overlay_scaled, (self._overlay_x, 0))

        pygame.display.flip()