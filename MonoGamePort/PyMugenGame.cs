using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using PyMugen.Managers;
using PyMugen.GameStates;

namespace PyMugen;

public sealed class PyMugenGame : Game
{
    private readonly GraphicsDeviceManager _graphics;
    private SpriteBatch _spriteBatch = null!;
    private readonly GameServiceProvider _services = GameServiceProvider.Instance;

    public PyMugenGame()
    {
        _graphics = new GraphicsDeviceManager(this);
        Content.RootDirectory = "Content";
        IsMouseVisible = true;

        _graphics.PreferredBackBufferWidth = 1280;
        _graphics.PreferredBackBufferHeight = 720;
        _graphics.ApplyChanges();
    }

    protected override void Initialize()
    {
        Window.Title = "pyMugen MonoGame Port";
        base.Initialize();
    }

    protected override void LoadContent()
    {
        _spriteBatch = new SpriteBatch(GraphicsDevice);

        _services.GraphicsManager.SetContentManager(Content);
        _services.ViewManager.GraphicsDevice = GraphicsDevice;
        _services.ViewManager.SetScreenSize(_graphics.PreferredBackBufferWidth, _graphics.PreferredBackBufferHeight);
        _services.DebugManager.SetFont(Content.Load<SpriteFont>("Fonts/DebugFont"));
        _services.GameStateManager.AddState("test", new TestState());
        _services.GameStateManager.ChangeState("test");

        base.LoadContent();
    }

    protected override void Update(GameTime gameTime)
    {
        if (GamePad.GetState(PlayerIndex.One).Buttons.Back == ButtonState.Pressed || Keyboard.GetState().IsKeyDown(Keys.Escape))
        {
            Exit();
        }

        var dt = (float)gameTime.ElapsedGameTime.TotalSeconds;

        _services.InputManager.Update();
        _services.DebugManager.Update(dt);
        _services.GameStateManager.Update(gameTime, dt);

        base.Update(gameTime);
    }

    protected override void Draw(GameTime gameTime)
    {
        GraphicsDevice.Clear(Color.CornflowerBlue);

        var spriteBatchStarted = false;
        try
        {
            _spriteBatch.Begin();
            spriteBatchStarted = true;
            _services.GameStateManager.Draw(_spriteBatch);
            _services.DebugManager.Draw(_spriteBatch, _services.ViewManager);
        }
        finally
        {
            if (spriteBatchStarted)
            {
                _spriteBatch.End();
            }
        }

        base.Draw(gameTime);
    }
}
