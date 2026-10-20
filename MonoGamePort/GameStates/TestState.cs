using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using PyMugen.GameObjects;

namespace PyMugen.GameStates;

public sealed class TestState : GameState
{
    private readonly GameObject _demoSprite;

    public TestState()
    {
        _demoSprite = new GameObject(new Vector2(200, 300));
    }

    public override void Enter()
    {
        GameObjects.Clear();
        GameObjects.Add(_demoSprite);
    }

    public override void Draw(SpriteBatch spriteBatch)
    {
        base.Draw(spriteBatch);
    }
}
