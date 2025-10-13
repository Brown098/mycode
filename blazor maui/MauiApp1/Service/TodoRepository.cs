using SQLite;
using MauiApp1.Models;

namespace MauiApp1.Service
{
    public class TodoRepository
    {
        private readonly SQLiteAsyncConnection _db;

        public TodoRepository(string dbPath)
        {
            _db = new SQLiteAsyncConnection(dbPath);
            _db.CreateTableAsync<TodoItem>().Wait();
        }

        public Task<List<TodoItem>> GetAllAsync() => _db.Table<TodoItem>().ToListAsync();

        public Task AddAsync(TodoItem item) => _db.InsertAsync(item);

        public Task UpdateAsync(TodoItem item) => _db.UpdateAsync(item);

        public Task DeleteAsync(TodoItem item) => _db.DeleteAsync(item);
    }
}
