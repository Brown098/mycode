using CommunityToolkit.Maui;
using Microsoft.Extensions.Logging;
using Plugin.LocalNotification;
using System.ComponentModel.Design;
using ToDoApp.Services;
using ToDoApp.ViewModels;


namespace ToDoApp;


public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        builder
        .UseMauiApp<App>()
        .UseMauiCommunityToolkit()
        .ConfigureFonts(fonts =>
        {
            fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
        });


        // services
        string dbPath = Path.Combine(FileSystem.AppDataDirectory, "todo.db");
        builder.Services.AddSingleton(new TodoRepository(dbPath));
        builder.Services.AddSingleton<TodoService>();
        builder.Services.AddSingleton<ApiSyncService>();
        builder.Services.AddSingleton<NotificationService>();
        builder.Services.AddSingleton<ThemeService>();
        builder.Services.AddSingleton<PreferencesService>();


        // viewmodels
        builder.Services.AddSingleton<TodoViewModel>();
        builder.Services.AddSingleton<SettingsViewModel>();


        builder.Services.AddMauiBlazorWebView();
#if DEBUG
        builder.Logging.AddDebug();
#endif
        return builder.Build();
    }
}