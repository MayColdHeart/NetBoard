using Microsoft.EntityFrameworkCore;
using NetboardApi.Data;

namespace NetboardApi.Startup;

public static class RequestPipelineConfig
{
    public static void StartDatabase(this WebApplication app)
    {
        using var scope = app.Services.CreateScope();
        var dbContext = scope.ServiceProvider.GetRequiredService<NetboardDbContext>();
        dbContext.Database.Migrate();
    }
}