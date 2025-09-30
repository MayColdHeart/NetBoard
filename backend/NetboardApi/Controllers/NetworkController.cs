using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using NetboardApi.Data;
using NetboardApi.Dtos.TrafficWindowDtos;
using NetboardApi.Hubs;
using NetboardApi.Interfaces;
using NetboardApi.Models;

namespace NetboardApi.Controllers;

[ApiController]
[Route("[controller]")]
public class NetworkController : ControllerBase
{
    private readonly ILogger<NetworkController> _logger;
    private readonly INetworkService _networkService;
    private readonly IHubContext<NetworkTrafficHub, INetworkTrafficClient> _hubContext;

    public NetworkController(
        ILogger<NetworkController> logger, 
        INetworkService networkService,
        IHubContext<NetworkTrafficHub, INetworkTrafficClient> hubContext)
    {
        _logger = logger;
        _networkService = networkService;
        _hubContext = hubContext;
    }
    
    [HttpGet("traffic")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public async Task<IActionResult> Get()
    {
        var devicesTraffic = await _networkService.GetTotalDeviceTrafficListAsync();
        return Ok(devicesTraffic);
    }
    
    [HttpPost("traffic-window")]
    [ProducesResponseType(StatusCodes.Status201Created)]
    public async Task<IActionResult> Post([FromBody] CreateTrafficWindowDto trafficWindowDto)
    {
        if (string.IsNullOrWhiteSpace(trafficWindowDto.DeviceIp))
        {
            return BadRequest("DeviceIp is required.");
        }
        if (string.IsNullOrWhiteSpace(trafficWindowDto.ProtocolName))
        {
            return BadRequest("ProtocolName is required.");
        }
        
        var createdTrafficWindow = await _networkService.CreateTrafficWindowAsync(trafficWindowDto);
        await _hubContext.Clients.All.ReceiveTraffic(createdTrafficWindow);
        
        return Created();
    }
}