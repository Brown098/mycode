using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi;


using TodoApi.Data;
using TodoApi.Hubs;

var builder = WebApplication.CreateBuilder(args);

// Add services
builder.Services.AddControllers();
builder.Services.AddDbContext<TodoDbContext>(options =>
    options.UseSqlite("Data Source=todos.db"));
builder.Services.AddSignalR();

// Ìí¼Ó Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo { Title = "TodoApi", Version = "v1" });
});

var app = builder.Build();

// Configure middleware
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c =>
    {
        c.SwaggerEndpoint("/swagger/v1/swagger.json", "TodoApi v1");
    });
}

app.UseHttpsRedirection();
app.UseAuthorization();

app.MapControllers();
app.MapHub<TodoHub>("/todoHub");

app.Run();
