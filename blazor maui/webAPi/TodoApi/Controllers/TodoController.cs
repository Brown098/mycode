using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TodoApi.Data;
using TodoApi.Models;
using TodoApi.Hubs;
using Microsoft.AspNetCore.SignalR;

namespace TodoApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TodoController : ControllerBase
    {
        private readonly TodoDbContext _context;
        private readonly IHubContext<TodoHub> _hub;

        public TodoController(TodoDbContext context, IHubContext<TodoHub> hub)
        {
            _context = context;
            _hub = hub;
        }

        // GET: api/todo
        [HttpGet]
        public async Task<ActionResult<IEnumerable<TodoItem>>> GetTodos()
        {
            return await _context.Todos.OrderByDescending(t => t.CreatedAt).ToListAsync();
        }

        // GET: api/todo/5
        [HttpGet("{id}")]
        public async Task<ActionResult<TodoItem>> GetTodoItem(int id)
        {
            var todo = await _context.Todos.FindAsync(id);
            if (todo == null) return NotFound();
            return todo;
        }

        // POST: api/todo
        [HttpPost]
        public async Task<ActionResult<TodoItem>> PostTodoItem(TodoItem item)
        {
            _context.Todos.Add(item);
            await _context.SaveChangesAsync();

            // SignalR 通知
            await _hub.Clients.All.SendAsync("TodoAdded", $"新任务：{item.Title}");

            return CreatedAtAction(nameof(GetTodoItem), new { id = item.Id }, item);
        }

        // PUT: api/todo/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutTodoItem(int id, TodoItem item)
        {
            if (id != item.Id) return BadRequest();

            _context.Entry(item).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
                await _hub.Clients.All.SendAsync("TodoUpdated", $"任务 {id} 已更新");
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!_context.Todos.Any(e => e.Id == id))
                    return NotFound();
                else
                    throw;
            }

            return NoContent();
        }

        // DELETE: api/todo/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteTodoItem(int id)
        {
            var todo = await _context.Todos.FindAsync(id);
            if (todo == null) return NotFound();

            _context.Todos.Remove(todo);
            await _context.SaveChangesAsync();

            await _hub.Clients.All.SendAsync("TodoDeleted", $"任务 {id} 已删除");
            return NoContent();
        }
    }
}
