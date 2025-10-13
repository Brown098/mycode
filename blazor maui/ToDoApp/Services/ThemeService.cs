namespace ToDoApp.Services;


public class ThemeService
{
    public void Apply(string theme)
    {
        App.Current.UserAppTheme = theme == "Dark" ? AppTheme.Dark : AppTheme.Light;
    }
}
