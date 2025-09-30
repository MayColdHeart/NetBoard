using NetboardApi.Data;
using NetboardApi.Dtos.TrafficWindowDtos;
using NetboardApi.Interfaces;
using NetboardApi.Mappers;
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

    public async Task<TrafficWindowDto> CreateTrafficWindowAsync(CreateTrafficWindowDto createTrafficWindowDto)
    {
        var transaction = await _dbContext.Database.BeginTransactionAsync();
        
        var device = _dbContext.Devices.FirstOrDefault(d => d.Ip == createTrafficWindowDto.DeviceIp);
        if (device is null)
        {
            device = new Device
            {
                Ip = createTrafficWindowDto.DeviceIp,
                CreatedAt = DateTimeOffset.UtcNow,
                UpdatedAt = DateTimeOffset.UtcNow
            };
            _dbContext.Devices.Add(device);
            await _dbContext.SaveChangesAsync();
        }
        
        var protocol = _dbContext.Protocols.FirstOrDefault(p => p.Name.ToUpper() == createTrafficWindowDto.ProtocolName.ToUpper());
        if (protocol is null)
        {
            protocol = new Protocol
            {
                Name = createTrafficWindowDto.ProtocolName.ToUpper(),
            };
            _dbContext.Protocols.Add(protocol);
            await _dbContext.SaveChangesAsync();
        }
        
        var trafficWindowModel = new TrafficWindow
        {
            DeviceId = device.Id,
            ProtocolId = protocol.Id,
            TotalSizeKbps = createTrafficWindowDto.TotalSizeKbps,
            UploadSizeKbps = createTrafficWindowDto.UploadSizeKbps,
            DownloadSizeKbps = createTrafficWindowDto.DownloadSizeKbps,
            CreatedAt = DateTimeOffset.UtcNow
        };

        _dbContext.TrafficWindows.Add(trafficWindowModel);
        await _dbContext.SaveChangesAsync();
        
        await transaction.CommitAsync();

        var createdTrafficWindowDto = trafficWindowModel.ToTrafficWindowDto();
        return createdTrafficWindowDto;
    }
}