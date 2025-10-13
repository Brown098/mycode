using Microsoft.Maui.Storage;


namespace ToDoApp.Services;


public class PreferencesService
{
    private const string ThemeKey = "app_theme";
    public void SetTheme(string v) => Preferences.Set(ThemeKey, v);
    public string GetTheme() => Preferences.Get(ThemeKey, "Light");
}