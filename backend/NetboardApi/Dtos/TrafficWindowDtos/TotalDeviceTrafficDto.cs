namespace NetboardApi.Dtos.TrafficWindowDtos;

public record TotalDeviceTrafficDto
{
    public string DeviceIp { get; init; } = string.Empty;
    public string Protocol { get; init; } = string.Empty;
    public int TotalSizeKbps { get; init; }
    public int UploadSizeKbps { get; init; }
    public int DownloadSizeKbps { get; init; }
}