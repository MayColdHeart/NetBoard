using Microsoft.EntityFrameworkCore;
using NetboardApi.Data;
using NetboardApi.Hubs;
using NetboardApi.Startup;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();
builder.Services.AddRouting(options => options.LowercaseUrls = true);

// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

builder.Services.AddPostgresDbContext(builder.Configuration);

builder.Services.AddSignalR();

builder.Services.AddDependencyInjectionServices();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseOpenApi();
    app.StartDatabase();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapHub<NetworkTrafficHub>("/network-hub");
app.MapControllers();

app.Run();