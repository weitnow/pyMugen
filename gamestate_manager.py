from decorators import singleton

@singleton
class GameStateManager:
    def __init__(self):
        self.states = {}         # map name → GameState
        self.current_state = None

    def add_state(self, name: str, state):
        self.states[name] = state

    def change_state(self, name: str):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states.get(name)
        if self.current_state:
            self.current_state.enter()
        else:
            raise ValueError(f"State '{name}' does not exist!")

    def handle_event(self, event):
        if self.current_state:
            self.current_state.handle_event(event)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)

    def draw(self):
        if self.current_state:
            self.current_state.draw()

    def debug_draw(self):
        if self.current_state:
            self.current_state.debug_draw()
