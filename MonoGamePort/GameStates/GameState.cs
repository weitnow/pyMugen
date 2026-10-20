using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using PyMugen.GameObjects;

namespace PyMugen.GameStates;

public abstract class GameState
{
    protected readonly List<GameObject> _gameObjects = new();

    protected void AddGameObject(GameObject gameObject)
    {
        _gameObjects.Add(gameObject);
    }

    public virtual void Enter() { }
    public virtual void Exit() { }
    public virtual void HandleInput() { }
    public virtual void Update(GameTime gameTime, float dt)
    {
        foreach (var gameObject in _gameObjects)
        {
            gameObject.Update(gameTime, dt);
        }
    }

    public virtual void Draw(SpriteBatch spriteBatch)
    {
        foreach (var gameObject in _gameObjects)
        {
            gameObject.Draw(spriteBatch);
        }
    }
}
