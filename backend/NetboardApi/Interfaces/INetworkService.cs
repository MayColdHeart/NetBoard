using NetboardApi.Dtos.TrafficWindowDtos;

namespace NetboardApi.Interfaces;

public interface INetworkService
{
    Task<TrafficWindowDto> CreateTrafficWindowAsync(CreateTrafficWindowDto createTrafficWindowDto);
}