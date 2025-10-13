using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using ToDoApp.Services;


namespace ToDoApp.ViewModels;


public partial class SettingsViewModel : ObservableObject
{
    private readonly PreferencesService _prefs;
    private readonly ThemeService _theme;


    [ObservableProperty]
    private string currentTheme;


    public SettingsViewModel(PreferencesService prefs, ThemeService theme)
    {
        _prefs = prefs;
        _theme = theme;
        currentTheme = _prefs.GetTheme();
    }


    [RelayCommand]
    public void ToggleTheme()
    {
        currentTheme = currentTheme == "Light" ? "Dark" : "Light";
        _prefs.SetTheme(currentTheme);
        _theme.Apply(currentTheme);
    }
}