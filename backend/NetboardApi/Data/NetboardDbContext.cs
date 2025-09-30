using System.Reflection;
using Microsoft.EntityFrameworkCore;
using NetboardApi.Models;

namespace NetboardApi.Data;

public class NetboardDbContext : DbContext
{
    public NetboardDbContext(DbContextOptions<NetboardDbContext> options) : base(options)
    {
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }
    
    public DbSet<Device> Devices { get; set; }
    public DbSet<Protocol> Protocols { get; set; }
    public DbSet<TrafficWindow> TrafficWindows { get; set; }
}