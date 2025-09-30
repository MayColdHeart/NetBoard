using Microsoft.AspNetCore.SignalR;
using NetboardApi.Dtos.TrafficWindowDtos;

namespace NetboardApi.Hubs;

public interface INetworkTrafficClient
{
    Task ReceiveTraffic(TrafficWindowDto trafficWindow);
}

public class NetworkTrafficHub : Hub<INetworkTrafficClient>
{
    public async Task SendTraffic(TrafficWindowDto trafficWindow)
    {
        await Clients.All.ReceiveTraffic(trafficWindow);
    }
}