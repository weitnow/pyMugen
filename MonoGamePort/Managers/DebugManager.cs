using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace PyMugen.Managers;

public sealed class DebugManager
{
    private SpriteFont? _font;

    public bool DebugOn { get; set; }

    public void Bind(ServiceProvider serviceProvider)
    {
        // no-op binding retained to mirror the Python architecture
    }

    public void SetFont(SpriteFont font)
    {
        _font = font;
    }

    public void Update(float dt)
    {
    }

    public void Draw(SpriteBatch spriteBatch, ViewManager viewManager)
    {
        if (!DebugOn || _font is null)
        {
            return;
        }

        spriteBatch.DrawString(_font, "pyMugen MonoGame debug", new Vector2(20, 20), Color.White);
    }
}
