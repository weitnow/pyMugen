using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Content;
using Microsoft.Xna.Framework.Graphics;

namespace PyMugen.Managers;

public sealed class GraphicsManager
{    private ContentManager? _contentManager;
    private readonly Dictionary<string, Texture2D> _textures = new();

    public void SetContentManager(ContentManager contentManager)
    {
        _contentManager = contentManager;
    }

    public Texture2D LoadTexture(string key, string assetName)
    {
        if (_contentManager is null)
        {
            throw new InvalidOperationException("ContentManager has not been initialized.");
        }

        if (_textures.TryGetValue(key, out var existing))
        {
            return existing;
        }

        var texture = _contentManager.Load<Texture2D>(assetName);
        _textures[key] = texture;
        return texture;
    }
}
