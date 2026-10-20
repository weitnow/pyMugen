using Microsoft.Xna.Framework.Input;

namespace PyMugen.Managers;

public enum Action
{
    Left,
    Right,
    Up,
    Down,
    A,
    B,
    C,
    D
}

public sealed class InputManager
{
    private KeyboardState _previousKeyboardState;
    private KeyboardState _currentKeyboardState;

    public void Update()
    {
        _previousKeyboardState = _currentKeyboardState;
        _currentKeyboardState = Keyboard.GetState();
    }

    public bool IsPressed(Keys key)
    {
        return _currentKeyboardState.IsKeyDown(key) && _previousKeyboardState.IsKeyUp(key);
    }

    public bool IsDown(Keys key)
    {
        return _currentKeyboardState.IsKeyDown(key);
    }
}
