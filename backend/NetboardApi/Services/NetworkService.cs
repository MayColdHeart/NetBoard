using NetboardApi.Data;
using NetboardApi.Dtos.TrafficWindowDtos;
using NetboardApi.Interfaces;
using NetboardApi.Models;

namespace NetboardApi.Services;

public class NetworkService : INetworkService
{
    private readonly ILogger<NetworkService> _logger;
    private readonly NetboardDbContext _dbContext;
    
    public NetworkService(ILogger<NetworkService> logger, NetboardDbContext dbContext)
    {
        _logger = logger;
        _dbContext = dbContext;
    }

    public async Task CreateTrafficWindowAsync(CreateTrafficWindowDto trafficWindowDto)
    {
        var transaction = await _dbContext.Database.BeginTransactionAsync();
        
        var device = _dbContext.Devices.FirstOrDefault(d => d.Ip == trafficWindowDto.DeviceIp);
        if (device is null)
        {
            device = new Device
            {
                Ip = trafficWindowDto.DeviceIp,
                CreatedAt = DateTimeOffset.UtcNow,
                UpdatedAt = DateTimeOffset.UtcNow
            };
            _dbContext.Devices.Add(device);
            await _dbContext.SaveChangesAsync();
        }
        
        var protocol = _dbContext.Protocols.FirstOrDefault(p => p.Name.ToUpper() == trafficWindowDto.ProtocolName.ToUpper());
        if (protocol is null)
        {
            protocol = new Protocol
            {
                Name = trafficWindowDto.ProtocolName.ToUpper(),
            };
            _dbContext.Protocols.Add(protocol);
            await _dbContext.SaveChangesAsync();
        }
        
        var trafficWindow = new TrafficWindow
        {
            DeviceId = device.Id,
            ProtocolId = protocol.Id,
            TotalSizeKbps = trafficWindowDto.TotalSizeKbps,
            UploadSizeKbps = trafficWindowDto.UploadSizeKbps,
            DownloadSizeKbps = trafficWindowDto.DownloadSizeKbps,
            CreatedAt = DateTimeOffset.UtcNow
        };

        _dbContext.TrafficWindows.Add(trafficWindow);
        await _dbContext.SaveChangesAsync();
        
        await transaction.CommitAsync();
    }
}