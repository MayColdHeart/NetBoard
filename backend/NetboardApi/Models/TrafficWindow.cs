namespace NetboardApi.Models;

public class TrafficWindow
{
    public int Id { get; set; }
    public string SourceIP { get; set; } = string.Empty;
    public int TotalSizeBytes { get; set; }
    public DateTimeOffset CreatedAt { get; set; }
    public int ProtocolId { get; set; }
    
    public Protocol Protocol { get; set; } = null!;
}