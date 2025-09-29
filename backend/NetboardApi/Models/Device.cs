namespace NetboardApi.Models;

public class Device
{
    public int Id { get; set; }
    public string Hostname { get; set; } = string.Empty;
    public string Ip { get; set; } = string.Empty;
    public DateTimeOffset CreatedAt { get; set; }
    public DateTimeOffset UpdatedAt { get; set; }
}