namespace NetboardApi.Dtos.TrafficWindowDtos;

public sealed record CreateTrafficWindowDto
{
    public string DeviceIp { get; init; } = string.Empty;
    public string ProtocolName { get; init; } = string.Empty;
    public double TotalSizeKbps { get; init; }
    public double UploadSizeKbps { get; init; }
    public double DownloadSizeKbps { get; init; }
}