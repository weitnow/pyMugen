import pygame
from decorators import singleton
from debug_manager import DebugManager

@singleton
class ViewManager:
    def __init__(self):
        self.GAME_VIEW_WIDTH = 209      
        self.GAME_VIEW_HEIGHT = 155
        self.OVERLAY_VIEWPORT = (145, 25, 209, 155)       # overlay transparent area (x, y, width, height)
        self.DEBUG_SCALE = 8            # scale factor for debug view
        self.AVAILABLE_RESOLUTIONS = [
            (640, 360),
            (960, 540),
            (1280, 720),
            (1920, 1080),
            (2560, 1440),
        ]
        self.CLEAR_COLOR = (30, 30, 30) # background color for game view
        self.current_resolution_index = 3  # start with 1920x1080
        self.fullscreen_enabled = False
        self.show_overlay = True


        # Game and Debug surfaces, open for public access
        self.game_surface = pygame.Surface((self.GAME_VIEW_WIDTH, self.GAME_VIEW_HEIGHT))
        self.debug_surface = pygame.Surface(
            (self.GAME_VIEW_WIDTH * self.DEBUG_SCALE, self.GAME_VIEW_HEIGHT * self.DEBUG_SCALE), 
            pygame.SRCALPHA
        )

        # Pre-calculate aspect ratio
        self._game_aspect = self.GAME_VIEW_WIDTH / self.GAME_VIEW_HEIGHT

        # create initial window
        self._apply_display_mode()

        # overlay
        self.overlay_image = pygame.image.load("assets/Graphics/Aseprite/overlay.png").convert_alpha()
        self.overlay_screen_rect = pygame.Rect(*self.OVERLAY_VIEWPORT)
        
        # Cache for scaled surfaces and calculations
        self._cached_overlay_scaled = None
        self._cached_dimensions = None  # (new_width, new_height)
        self._offset = None  # (offset_x, offset_y)
        self._overlay_x = 0
        self._last_window_size = None
        self._last_overlay_state = None
        
        # Reusable rect to avoid recreating
        self.render_rect = pygame.Rect(0, 0, 0, 0)

        self.debug_manager = DebugManager() # get singleton instance 
        self.debug_manager.set_view_manager(self) # inform debug manager about view manager

    def update(self, dt):
        pass # dt is now in seconds

    # --- Internal helper ---
    def _apply_display_mode(self):
        if self.fullscreen_enabled:
            self.fullscreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            width, height = self.AVAILABLE_RESOLUTIONS[self.current_resolution_index]
            self.fullscreen = pygame.display.set_mode((width, height))
        self.screen_rect = self.fullscreen.get_rect()
        pygame.display.set_caption(f"Game View - {'Fullscreen' if self.fullscreen_enabled else f'{self.fullscreen.get_width()}x{self.fullscreen.get_height()}'}")
        
        # Invalidate cache on mode change
        self._last_window_size = None
        self._cached_dimensions = None

    # --- Toggle fullscreen/windowed ---
    def toggle_fullscreen(self):
        self.fullscreen_enabled = not self.fullscreen_enabled
        self._apply_display_mode()

    # --- Toggle overlay ---
    def toggle_overlay(self):
        self.show_overlay = not self.show_overlay

    # --- Cycle through resolutions ---
    def cycle_resolution(self):
        if not self.fullscreen_enabled:
            self.current_resolution_index = (self.current_resolution_index + 1) % len(self.AVAILABLE_RESOLUTIONS)
            self._apply_display_mode()

    # --- Convert GameView coordinates to DebugView ---
    def to_debug_coords(self, x: float, y: float):
        return x * self.DEBUG_SCALE, y * self.DEBUG_SCALE
    
    def clear(self):
        self.game_surface.fill(self.CLEAR_COLOR)    
        self.debug_surface.fill((0, 0, 0, 0))

    # --- Draw everything ---
    def draw_to_screen(self):
        window_w, window_h = self.fullscreen.get_size()
        current_window_size = (window_w, window_h)
        current_overlay_state = self.show_overlay
        
        # Check if we need to recalculate scaling/positioning
        needs_recalc = (
            self._last_window_size != current_window_size or
            self._last_overlay_state != current_overlay_state
        )
        
        if needs_recalc:
            self._last_window_size = current_window_size
            self._last_overlay_state = current_overlay_state
            
            # --- calculate rendering area depending on overlay ---
            if self.show_overlay:
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

            if target_aspect > self._game_aspect:
                scale = self.render_rect.h / self.GAME_VIEW_HEIGHT
                new_width = int(self.GAME_VIEW_WIDTH * scale)
                new_height = self.render_rect.h
                offset_x = self.render_rect.x + (self.render_rect.w - new_width) // 2
                offset_y = self.render_rect.y
            else:
                scale = self.render_rect.w / self.GAME_VIEW_WIDTH
                new_width = self.render_rect.w
                new_height = int(self.GAME_VIEW_HEIGHT * scale)
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

        if self.debug_manager.debug_on:
            # Scale debug surface (content changes when debug is active)
            debug_scaled = pygame.transform.scale(self.debug_surface, (new_width, new_height))
            debug_scaled.set_alpha(160)
            self.fullscreen.blit(debug_scaled, (offset_x, offset_y))

        if self.show_overlay:
            # Use cached scaled overlay
            self.fullscreen.blit(self._cached_overlay_scaled, (self._overlay_x, 0))

        pygame.display.flip()