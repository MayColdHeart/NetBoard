namespace NetboardApi.Dtos.TrafficWindowDtos;

public record TrafficWindowDto
{
    public int Id { get; init; }
    public int DeviceIp { get; init; }
    public string Protocol { get; init; } = string.Empty;
    public int TotalSizeKbps { get; init; }
    public int UploadSizeKbps { get; init; }
    public int DownloadSizeKbps { get; init; }
    public DateTimeOffset CreatedAt { get; init; }
}