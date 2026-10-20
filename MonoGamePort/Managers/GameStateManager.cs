using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using PyMugen.GameStates;

namespace PyMugen.Managers;

public sealed class GameStateManager
{
    private readonly Dictionary<string, GameState> _states = new();
    public GameState? CurrentState { get; private set; }

    public void AddState(string name, GameState state)
    {
        _states[name] = state;
    }

    public void ChangeState(string name)
    {
        if (CurrentState is not null)
        {
            CurrentState.Exit();
        }

        if (!_states.TryGetValue(name, out var nextState))
        {
            throw new InvalidOperationException($"State '{name}' does not exist!");
        }

        CurrentState = nextState;
        CurrentState.Enter();
    }

    public void Update(GameTime gameTime, float dt)
    {
        CurrentState?.Update(gameTime, dt);
    }

    public void Draw(SpriteBatch spriteBatch)
    {
        CurrentState?.Draw(spriteBatch);
    }
}
