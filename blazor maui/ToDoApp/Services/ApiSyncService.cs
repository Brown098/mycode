using System.Net.Http.Json;
using ToDoApp.Models;
namespace ToDoApp.Services;

public class ApiSyncService
{
    private readonly HttpClient _client;
    public ApiSyncService()
    {
        _client = new HttpClient { BaseAddress = new Uri("http://198.46.138.143:5230") };
    }
    public async Task SyncAsync(IEnumerable<TodoItem> items)
    {
        foreach (var it in items)
            await _client.PostAsJsonAsync("api/todo", it);
    }
    public async Task<List<TodoItem>> FetchAsync()
    {
        return await _client.GetFromJsonAsync<List<TodoItem>>("api/todo") ?? new List<TodoItem>();
    }
}
