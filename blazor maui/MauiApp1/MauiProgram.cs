using Microsoft.Extensions.Logging;
using MauiApp1.Service;
namespace MauiApp1
{
    public static class MauiProgram
    {
        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder();
            builder
                .UseMauiApp<App>()
                .ConfigureFonts(fonts =>
                {
                    fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                });

            builder.Services.AddScoped(sp => new HttpClient
            {
                BaseAddress = new Uri("https://lyon.eu.org/metrics")
            });

            builder.Services.AddMauiBlazorWebView();

#if DEBUG
    		builder.Services.AddBlazorWebViewDeveloperTools();
            builder.Services.AddSingleton<AppState>();

            string dbPath = Path.Combine(FileSystem.AppDataDirectory, "todo.db");
            builder.Services.AddSingleton(new TodoRepository(dbPath));
            builder.Logging.AddDebug();
#endif

            return builder.Build();
        }
    }
}
