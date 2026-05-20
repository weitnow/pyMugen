import pygame
import time
import psutil
from decorators import singleton

@singleton
class DebugManager:
    def __init__(self):
        self.debug_on = True
        self.debug_text = True
        self.DRAW_MOUSE_POS = True

        self._sp = None  # set by ServiceProvider after all managers are initialized

        self._small_font = pygame.font.Font(None, 12)
        self._last_time = time.time()
        self._fps = 0
        self._frame_time_ms = 0

        self._last_system_info_update = 0
        self._system_info_update_interval = 3.0
        self._cpu_percent = 0
        self._mem_used_mb = 0
        self._process = psutil.Process()

        self._rect_cache = {}  # key: (w, h, color, alpha)

        # Panel state — updated by begin_panel(), used by line()
        self._debug_start_x = 0
        self._debug_start_y = 0
        self._debug_cursor_x = 0
        self._debug_cursor_y = 0
        self._debug_line_height = 0
        self._upper_section_max_y = 0
        self._lower_section_min_y = 0
        self._lower_section_max_y = 0
        self._debug_column_width = 0
        self._debug_max_columns = 0
        self._current_column = 0
        self._in_middle_section = False
        self._in_lower_section = False

        # Set by bind_view_manager()
        self._view_manager = None
        self._game_surface = None
        self._game_view_width = 0
        self._game_view_height = 0
        self._debug_overlay = None
        self._camera = None

    def bind_service_provider(self, sp):
        self._sp = sp

        if self._sp is not None:
            self.bind_view_manager(self._sp.view_manager)

    def bind_view_manager(self, view_manager):
        self._view_manager = view_manager
        self._game_surface = view_manager.game_surface
        self._game_view_width = view_manager.GAME_VIEW_WIDTH
        self._game_view_height = view_manager.GAME_VIEW_HEIGHT
        self._debug_overlay = self._get_rect_surface(
            self._game_view_width, self._game_view_height, (0, 0, 0), 138
        )
        self._camera = view_manager.camera

    def update(self, dt):
        if not self.debug_on:
            return
        now = time.time()
        self._frame_time_ms = dt * 1000.0
        self._fps = 1.0 / dt if dt > 0 else 0
        self._last_time = now
        if now - self._last_system_info_update >= self._system_info_update_interval:
            self._update_system_info()
            self._last_system_info_update = now

    def debug_draw(self):
        if not self.debug_on:
            return

        self._game_surface.blit(self._debug_overlay, (0, 0))

        self.begin_panel(8, 8)

        self.line(f"FPS: {self._fps:.1f}")
        self.line(f"CPU: {self._cpu_percent:.1f}%")
        self.line(f"RAM: {self._mem_used_mb:.1f} MB")
        self.line(f"CAMpos: ({self._camera.x}, {self._camera.y})")

        if self.DRAW_MOUSE_POS:
            mx, my = pygame.mouse.get_pos()
            self.line(f"MOUSEpos: ({mx}, {my})")


        for i in range(138):
            self.line(f"Debug line {i+1}")

    def draw_debug_text(self, x=8, y=8, text="", color=(255, 255, 0)):
        if not self.debug_on or self._view_manager is None:
            return
        img = self._small_font.render(text, True, color)
        self._view_manager.game_surface.blit(img, (x, y))

    def draw_rect_overlay(self, x, y, width, height, color, alpha=128):
        surf = self._get_rect_surface(width, height, color, alpha)
        self._game_surface.blit(surf, (x, y))

    def begin_panel(
        self,
        x=8,
        y=8,
        line_height=None,
        upper_section_max_y=78,
        lower_section_min_y=420,
        lower_section_max_y=530,
        column_width=150,
        max_columns=6
    ):
        self._debug_start_x = x
        self._debug_start_y = y
        self._debug_cursor_x = x
        self._debug_cursor_y = y
        self._upper_section_max_y = upper_section_max_y
        self._lower_section_min_y = lower_section_min_y
        self._lower_section_max_y = lower_section_max_y
        self._debug_column_width = column_width
        self._debug_max_columns = max_columns
        self._current_column = 0
        self._in_middle_section = False
        self._in_lower_section = False

        if line_height is None:
            line_height = self._small_font.get_height() + 2
        self._debug_line_height = line_height

    def line(self, text="", color=(255, 255, 0)):
        self.draw_debug_text(
            x=self._debug_cursor_x,
            y=self._debug_cursor_y,
            text=text,
            color=color
        )

        self._debug_cursor_y += self._debug_line_height

        if not self._in_middle_section and not self._in_lower_section:
            if self._debug_cursor_y >= self._upper_section_max_y:
                if self._current_column < self._debug_max_columns - 1:
                    self._current_column += 1
                    self._debug_cursor_x += self._debug_column_width
                    self._debug_cursor_y = self._debug_start_y
                else:
                    self._in_middle_section = True
                    self._debug_cursor_x = self._debug_start_x
                    self._debug_cursor_y = self._upper_section_max_y
                    self._current_column = 0
        elif self._in_middle_section:
            if self._debug_cursor_y >= self._lower_section_min_y:
                self._in_middle_section = False
                self._in_lower_section = True
                self._debug_cursor_x = self._debug_start_x
                self._debug_cursor_y = self._lower_section_min_y
                self._current_column = 0
        else:
            if self._debug_cursor_y >= self._lower_section_max_y:
                if self._current_column < self._debug_max_columns - 1:
                    self._current_column += 1
                    self._debug_cursor_x += self._debug_column_width
                    self._debug_cursor_y = self._lower_section_min_y

    def _draw_fps_systeminfo(self, x, y):
        if not self.debug_on or self._view_manager is None:
            return
        text = f"FPS: {self._fps:.1f} | CPU: {self._cpu_percent:.1f}% | RAM: {self._mem_used_mb:.1f} MB"
        img = self._small_font.render(text, True, (255, 255, 0))
        self._view_manager.game_surface.blit(img, (x, y))

    def _update_system_info(self):
        self._cpu_percent = self._process.cpu_percent()
        mem_info = self._process.memory_info()
        self._mem_used_mb = mem_info.rss / (1024 * 1024)

    def _get_rect_surface(self, width, height, color, alpha):
        key = (width, height, color, alpha)
        if key not in self._rect_cache:
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            surf.fill((*color, alpha))
            self._rect_cache[key] = surf
        return self._rect_cache[key]