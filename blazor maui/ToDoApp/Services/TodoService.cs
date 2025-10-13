using ToDoApp.Models;


namespace ToDoApp.Services;


public class TodoService
{
    private readonly TodoRepository _repo;
    public TodoService(TodoRepository repo) => _repo = repo;


    public Task<List<TodoItem>> GetAllAsync() => _repo.GetAllAsync();
    public Task AddAsync(TodoItem item) => _repo.AddAsync(item);
    public Task UpdateAsync(TodoItem item) => _repo.UpdateAsync(item);
    public Task DeleteAsync(int id) => _repo.DeleteAsync(new TodoItem { Id = id });
}
