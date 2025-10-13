using SQLite;
using ToDoApp.Models;


namespace ToDoApp.Services;


public class TodoRepository
{
    private readonly SQLiteAsyncConnection _db;
    public TodoRepository(string dbPath)
    {
        _db = new SQLiteAsyncConnection(dbPath);
        _db.CreateTableAsync<TodoItem>().Wait();
    }


    public Task<List<TodoItem>> GetAllAsync() => _db.Table<TodoItem>().OrderByDescending(x => x.CreatedAt).ToListAsync();
    public Task<TodoItem> GetAsync(int id) => _db.Table<TodoItem>().Where(x => x.Id == id).FirstOrDefaultAsync();
    public Task<int> AddAsync(TodoItem item) => _db.InsertAsync(item);
    public Task<int> UpdateAsync(TodoItem item) => _db.UpdateAsync(item);
    public Task<int> DeleteAsync(TodoItem item) => _db.DeleteAsync(item);
}