using NetboardApi.Dtos.TrafficWindowDtos;
using NetboardApi.Models;

namespace NetboardApi.Mappers;

public static class TrafficWindowMappers
{
    public static TrafficWindowDto ToTrafficWindowDto(this TrafficWindow trafficWindow)
    {
        return new TrafficWindowDto
        {
            Id = trafficWindow.Id,
            DeviceIp = trafficWindow.Device.Ip,
            Protocol = trafficWindow.Protocol.Name,
            TotalSizeKbps = trafficWindow.TotalSizeKbps,
            UploadSizeKbps = trafficWindow.UploadSizeKbps,
            DownloadSizeKbps = trafficWindow.DownloadSizeKbps,
            CreatedAt = trafficWindow.CreatedAt
        };
    }
}