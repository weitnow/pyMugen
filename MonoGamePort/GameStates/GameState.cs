using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using PyMugen.GameObjects;

namespace PyMugen.GameStates;

public abstract class GameState
{
    protected readonly List<GameObject> GameObjects = new();

    public virtual void Enter() { }
    public virtual void Exit() { }
    public virtual void HandleInput() { }
    public virtual void Update(GameTime gameTime, float dt)
    {
        foreach (var gameObject in GameObjects)
        {
            gameObject.Update(gameTime, dt);
        }
    }

    public virtual void Draw(SpriteBatch spriteBatch)
    {
        foreach (var gameObject in GameObjects)
        {
            gameObject.Draw(spriteBatch);
        }
    }
}
