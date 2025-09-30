using NetboardApi.Dtos.TrafficWindowDtos;

namespace NetboardApi.Interfaces;

public interface INetworkService
{
    Task CreateTrafficWindowAsync(CreateTrafficWindowDto trafficWindowDto);
}