namespace NetboardApi.Models;

public class TrafficWindow
{
    public int Id { get; set; }
    public int DeviceId { get; set; }
    public int ProtocolId { get; set; }
    public int TotalSizeKbps { get; set; }
    public int UploadSizeKbps { get; set; }
    public int DownloadSizeKbps { get; set; }
    public DateTimeOffset CreatedAt { get; set; }
    
    public Protocol Protocol { get; set; } = null!;
    public Device Device { get; set; } = null!;
}