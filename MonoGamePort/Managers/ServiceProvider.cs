namespace PyMugen.Managers;

public sealed class GameServiceProvider
{
    private static GameServiceProvider? _instance;
    private static readonly object SyncRoot = new();

    public static GameServiceProvider Instance
    {
        get
        {
            lock (SyncRoot)
            {
                _instance ??= new GameServiceProvider();
                return _instance;
            }
        }
    }

    public GameStateManager GameStateManager { get; } = new();
    public InputManager InputManager { get; } = new();
    public DebugManager DebugManager { get; } = new();
    public GraphicsManager GraphicsManager { get; } = new();
    public SoundManager SoundManager { get; } = new();
    public SettingsManager SettingsManager { get; } = new();
    public ViewManager ViewManager { get; } = new();

    private GameServiceProvider()
    {
        DebugManager.Bind(this);
        ViewManager.Bind(this);
    }
}
