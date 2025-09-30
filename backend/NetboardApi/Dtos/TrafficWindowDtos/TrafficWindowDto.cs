namespace NetboardApi.Dtos.TrafficWindowDtos;

public record TrafficWindowDto
{
    public int Id { get; init; }
    public string DeviceIp { get; init; } = string.Empty;
    public string Protocol { get; init; } = string.Empty;
    public double TotalSizeKbps { get; init; }
    public double UploadSizeKbps { get; init; }
    public double DownloadSizeKbps { get; init; }
    public DateTimeOffset CreatedAt { get; init; }
}