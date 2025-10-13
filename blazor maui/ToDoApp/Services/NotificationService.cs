using Plugin.LocalNotification;


namespace ToDoApp.Services;


public class NotificationService
{
    public void Show(string title, string message)
    {
        var request = new NotificationRequest
        {
            NotificationId = new Random().Next(1000, 60000),
            Title = title,
            Description = message,
            Schedule = new NotificationRequestSchedule { NotifyTime = DateTime.Now.AddSeconds(1) }
        };
        LocalNotificationCenter.Current.Show(request);
    }
}
