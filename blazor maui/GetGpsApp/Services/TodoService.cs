using System;
using System.Collections.Generic;
using System.Text;
using GetGpsApp.Models;
namespace GetGpsApp.Services
{
    public class TodoService
    {
        public List<TodoItem> Items { get; set; }=new List<TodoItem>();
        public void Add(string title)
        {
            Items.Add(new TodoItem() { Title = title });
        }
        public void Remove(TodoItem item) { 
        
            Items.Remove(item);
        }


    }
}
