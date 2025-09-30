namespace NetboardApi.Dtos.TrafficWindowDtos;

public record TrafficWindowDto
{
    public int Id { get; init; }
    public int DeviceIp { get; init; }
    public int Protocol { get; init; }
    public int TotalSizeKbps { get; init; }
    public int UploadSizeKbps { get; init; }
    public int DownloadSizeKbps { get; init; }
    public DateTimeOffset CreatedAt { get; init; }
}