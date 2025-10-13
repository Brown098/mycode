using Microsoft.AspNetCore.SignalR;

namespace TodoApi.Hubs
{
    public class TodoHub : Hub
    {
        public async Task NotifyTodoAdded(string title)
        {
            await Clients.All.SendAsync("TodoAdded", $"新任务：{title}");
        }

        public async Task NotifyTodoUpdated(int id)
        {
            await Clients.All.SendAsync("TodoUpdated", $"任务 {id} 已更新");
        }

        public async Task NotifyTodoDeleted(int id)
        {
            await Clients.All.SendAsync("TodoDeleted", $"任务 {id} 已删除");
        }
    }
}
