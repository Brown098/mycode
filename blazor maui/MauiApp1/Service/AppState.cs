using System;
using System.Collections.Generic;
using System.Text;

namespace MauiApp1.Service
{
    public class AppState
    {
        public bool IsDarkTheme { get; set; } = false;
        public event Action? OnChange;

        public void ToggleTheme()
        {
            IsDarkTheme = !IsDarkTheme;
            OnChange?.Invoke();
        }
    }

}
