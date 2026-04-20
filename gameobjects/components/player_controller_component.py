from input_manager import InputManager, Action
from collections import deque
import time
from typing import Optional

# --- PlayerController ---
class PlayerController:
    def __init__(self, player_index: int, owner: any): # owner is the GameObject this controller is attached to
        self.player_index = player_index
        self.input_manager = InputManager()
        self.owner = owner
        self.specialmovelist = owner.specialmovelist
        
        # Current frame actions
        self.actions: dict[Action, bool] = {action: False for action in Action}
        
        # Detected special
        self.special_executed: Optional[str] = None
        
        # Simple input buffer: stores only new inputs as they happen
        self._input_sequence: deque[tuple[float, Action]] = deque()
        self._buffer_time: float = 0.7
        
        # Track last input to avoid duplicates
        self._last_input: Optional[Action] = None

        # Diagonal mappings
        self.DIAGONALS = {
            frozenset({Action.DOWN, Action.RIGHT}): Action.DOWN_RIGHT,
            frozenset({Action.DOWN, Action.LEFT}): Action.DOWN_LEFT,
            frozenset({Action.UP, Action.RIGHT}): Action.UP_RIGHT,
            frozenset({Action.UP, Action.LEFT}): Action.UP_LEFT,
        }

    def normalize_diagonals(self, actions: frozenset[Action]) -> frozenset[Action]:
        """Convert cardinal direction combinations into diagonal actions."""
        new_actions = set(actions)
        for combo, diagonal_action in self.DIAGONALS.items():
            if combo.issubset(actions):
                new_actions -= combo
                new_actions.add(diagonal_action)
        return frozenset(new_actions)

    def update(self, dt):
        """Update controller state - call once per frame."""
        pressed_actions = self.input_manager.get_pressed_actions(self.player_index)
        current_time = time.time()

        # Normalize diagonals
        pressed_actions = self.normalize_diagonals(frozenset(pressed_actions))

        # Update current actions dict
        for action in Action:
            self.actions[action] = action in pressed_actions

        # Add new inputs to sequence (only when they change)
        for action in pressed_actions:
            if action != self._last_input:
                self._input_sequence.append((current_time, action))
                self._last_input = action
                break  # Only track one new input per frame
        
        # If nothing pressed, reset last input
        if not pressed_actions:
            self._last_input = None

        # Clean old inputs from buffer
        while self._input_sequence and current_time - self._input_sequence[0][0] > self._buffer_time:
            self._input_sequence.popleft()

        # Clear previous special
        self.special_executed = None

        # Check for special moves
        self.check_specials()

    def check_specials(self):
        """Check if any special move pattern matches the input sequence."""
        if len(self._input_sequence) < 2:
            return
        
        # Extract just the actions from the sequence
        sequence = [action for _, action in self._input_sequence]
        
        # Check each special pattern
        for name, pattern in self.specialmovelist.items():
            pattern_len = len(pattern)
            
            # Check if the end of our sequence matches the pattern
            if len(sequence) >= pattern_len:
                if sequence[-pattern_len:] == pattern:
                    print(f"🎯 SPECIAL EXECUTED: {name}")
                    self.special_executed = name
                    # Clear buffer to prevent re-triggering
                    self._input_sequence.clear()
                    self._last_input = None
                    return  # Only one special per frame

    def is_action_pressed(self, action: Action) -> bool:
        """Check if an action is currently pressed."""
        return self.actions.get(action, False)

    def get_special_executed(self) -> Optional[str]:
        """Get the special executed this frame (if any)."""
        return self.special_executed