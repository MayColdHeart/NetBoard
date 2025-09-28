using Microsoft.EntityFrameworkCore;
using NetboardApi.Data;

namespace NetboardApi.Startup;

public static class DependenciesConfig
{
    public static IServiceCollection AddPostgresDbContext(this IServiceCollection services,
        IConfiguration configuration)
    {
        string? connectionString = configuration.GetConnectionString("DefaultConnection");
        services.AddDbContext<NetboardDbContext>(options => options.UseNpgsql(connectionString));
        
        return services;
    }
}