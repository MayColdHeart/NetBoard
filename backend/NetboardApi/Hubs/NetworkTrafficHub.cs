using Microsoft.AspNetCore.SignalR;
using NetboardApi.Dtos.TrafficWindowDtos;

namespace NetboardApi.Hubs;

public interface INetworkTrafficClient
{
    Task ReceiveTraffic(TrafficWindowDto trafficWindow);
}

public class NetworkTrafficHub : Hub<INetworkTrafficClient>
{
    private readonly ILogger<NetworkTrafficHub> _logger;
    
    public NetworkTrafficHub(ILogger<NetworkTrafficHub> logger)
    {
        _logger = logger;
    }
    
    public async Task SendTraffic(TrafficWindowDto trafficWindow)
    {
        _logger.LogInformation("Traffic sent. ConnectionId: {ConnectionId}", Context.ConnectionId);
        await Clients.All.ReceiveTraffic(trafficWindow);
    }

    public override async Task OnConnectedAsync()
    {
        _logger.LogInformation("Connection established. ConnectionId: {ConnectionId}", Context.ConnectionId);
        await base.OnConnectedAsync();
    }
    
    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        _logger.LogInformation("Connection closed. ConnectionId: {ConnectionId}", Context.ConnectionId);
        await base.OnDisconnectedAsync(exception);
    }
}