namespace PyMugen.Managers;

public sealed class ServiceProvider
{
    private static ServiceProvider? _instance;
    private static readonly object SyncRoot = new();

    public static ServiceProvider Instance
    {
        get
        {
            lock (SyncRoot)
            {
                _instance ??= new ServiceProvider();
                return _instance;
            }
        }
    }

    public GameStateManager GameStateManager { get; } = new();
    public InputManager InputManager { get; } = new();
    public DebugManager DebugManager { get; } = new();
    public GraphicManager GraphicManager { get; } = new();
    public SoundManager SoundManager { get; } = new();
    public SettingsManager SettingsManager { get; } = new();
    public ViewManager ViewManager { get; } = new();

    private ServiceProvider()
    {
        DebugManager.Bind(this);
        ViewManager.Bind(this);
    }
}
