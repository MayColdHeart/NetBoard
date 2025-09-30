namespace NetboardApi.Dtos.TrafficWindowDtos;

public record TotalDeviceTrafficDto
{
    public string DeviceIp { get; init; } = string.Empty;
    public string Protocol { get; init; } = string.Empty;
    public double TotalSizeKbps { get; init; }
    public double UploadSizeKbps { get; init; }
    public double DownloadSizeKbps { get; init; }
}