using Microsoft.AspNetCore.Cors.Infrastructure;
using Microsoft.EntityFrameworkCore;
using NetboardApi.Constants;
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
    
    public static IServiceCollection AddConfiguredCors(this IServiceCollection services)
    {
        //TODO: improve security
        CorsPolicy corsPolicy = new CorsPolicyBuilder()
            .WithOrigins(
                "http://localhost:5173"
            )
            .AllowAnyHeader()
            .AllowAnyMethod()
            .AllowCredentials()
            .Build();
        services.AddCors(options => {
            options.AddPolicy(CorsPolicyConstants.AllowSpecificOrigins, corsPolicy);
        });
        
        return services;
    }
}