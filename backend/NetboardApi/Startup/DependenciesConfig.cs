using Microsoft.EntityFrameworkCore;
using NetboardApi.Data;
using NetboardApi.Interfaces;
using NetboardApi.Services;

namespace NetboardApi.Startup;

public static class DependenciesConfig
{
    public static IServiceCollection AddDependencyInjectionServices(this IServiceCollection services)
    {
        services.AddScoped<INetworkService, NetworkService>();
        
        return services;
    }
    
    public static IServiceCollection AddPostgresDbContext(this IServiceCollection services,
        IConfiguration configuration)
    {
        string? connectionString = configuration.GetConnectionString("DefaultConnection");
        services.AddDbContext<NetboardDbContext>(options => options.UseNpgsql(connectionString));
        
        return services;
    }
}