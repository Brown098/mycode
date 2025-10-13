using System;
using System.Collections.Generic;
using System.Text;
using SQLite;

namespace MauiApp1.Models;
public class TodoItem
{
    [PrimaryKey , AutoIncrement]
    public int Id { get; set; }
    public string Title { get; set; } = "";
    public bool Done {  get; set; }=false;
    public DateTime CreatedAt { get; set; } = DateTime.Now;

}
