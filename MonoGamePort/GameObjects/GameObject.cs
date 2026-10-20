using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace PyMugen.GameObjects;

public class GameObject
{
    public Vector2 WorldPosition { get; set; }
    public Texture2D? Texture { get; set; }
    public Color Color { get; set; } = Color.White;

    public GameObject(Vector2 worldPosition)
    {
        WorldPosition = worldPosition;
    }

    public virtual void Update(GameTime gameTime, float dt)
    {
    }

    public virtual void Draw(SpriteBatch spriteBatch)
    {
        if (Texture is null)
        {
            return;
        }

        spriteBatch.Draw(Texture, WorldPosition, Color);
    }
}
