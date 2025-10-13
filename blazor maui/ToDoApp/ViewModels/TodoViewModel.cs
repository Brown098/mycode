using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using ToDoApp.Models;
using ToDoApp.Services;
using System.Collections.ObjectModel;
namespace ToDoApp.ViewModels;

public partial class TodoViewModel : ObservableObject
{
    private readonly TodoService _service;
    private readonly NotificationService _notify;
    public ObservableCollection<TodoItem> Items { get; } = new();
    [ObservableProperty]
    public string newTask = string.Empty;
    public TodoViewModel(TodoService service, NotificationService notify)
    {
        _service = service;
        _notify = notify;
        _ = LoadAsync();
    }
    private async Task LoadAsync()
    {
        var all = await _service.GetAllAsync();
        Items.Clear();
        foreach (var it in all) Items.Add(it);
    }
    [RelayCommand]
    public async Task AddAsync()
    {
        if (string.IsNullOrWhiteSpace(newTask)) return;
        var item = new TodoItem { Title = newTask, IsCompleted = false, CreatedAt = DateTime.UtcNow };
        await _service.AddAsync(item);
        Items.Insert(0, item);
        newTask = string.Empty;
        _notify.Show("任务添加", item.Title);
    }
    [RelayCommand]
    public async Task ToggleCompleteAsync(TodoItem item)
    {
        item.IsCompleted = !item.IsCompleted;
        await _service.UpdateAsync(item);
    }
    [RelayCommand]
    public async Task DeleteAsync(TodoItem item)
    {
        await _service.DeleteAsync(item.Id);
        Items.Remove(item);
    }
}
