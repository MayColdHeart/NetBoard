namespace NetboardApi.Dtos.TrafficWindowDtos;

public record TrafficWindowDto
{
    public int Id { get; set; }
    public int DeviceIp { get; set; }
    public int Protocol { get; set; }
    public int TotalSizeKbps { get; set; }
    public int UploadSizeKbps { get; set; }
    public int DownloadSizeKbps { get; set; }
    public DateTimeOffset CreatedAt { get; set; }
}