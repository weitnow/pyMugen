class GameState:
    """Base class for all game states."""

    def __init__(self, manager):
        self.manager = manager  # reference to the state manager

    def enter(self):
        """Called when the state is entered."""
        pass

    def exit(self):
        """Called when the state is exited."""
        pass

    def handle_event(self, event):
        """Handle pygame events."""
        pass

    def update(self, dt):
        """Update the state logic."""
        pass

    def draw(self, surface):
        """Draw the state to the given surface."""
        pass
