using System.Reflection;
using Microsoft.EntityFrameworkCore;

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
}