using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace PyMugen.Managers;

public sealed class ViewManager
{
    public GraphicsDevice? GraphicsDevice { get; set; }
    public Camera Camera { get; } = new();
    public Vector2 ScreenSize { get; private set; } = new(1280, 720);

    public void SetScreenSize(int width, int height)
    {
        ScreenSize = new Vector2(width, height);
    }

    public void Bind(GameServiceProvider serviceProvider)
    {
        // no-op binding retained to mirror the Python architecture
    }
}

public sealed class Camera
{
    public Vector2 Position { get; set; }

    public Vector2 Apply(Vector2 worldPosition)
    {
        return worldPosition - Position;
    }
}
