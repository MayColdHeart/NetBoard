namespace NetboardApi.Dtos.TrafficWindowDtos;

public sealed record CreateTrafficWindowDto
{
    public string DeviceIp { get; init; } = string.Empty;
    public string ProtocolName { get; init; } = string.Empty;
    public int TotalSizeKbps { get; init; }
    public int UploadSizeKbps { get; init; }
    public int DownloadSizeKbps { get; init; }
}