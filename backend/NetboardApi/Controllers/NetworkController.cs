using Microsoft.AspNetCore.Mvc;
using NetboardApi.Data;
using NetboardApi.Dtos.TrafficWindowDtos;
using NetboardApi.Interfaces;
using NetboardApi.Models;

namespace NetboardApi.Controllers;

[ApiController]
[Route("[controller]")]
public class NetworkController : ControllerBase
{
    private readonly ILogger<NetworkController> _logger;
    private readonly INetworkService _networkService;

    public NetworkController(ILogger<NetworkController> logger, INetworkService networkService)
    {
        _logger = logger;
        _networkService = networkService;
    }
    
    [HttpGet("traffic")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public IActionResult Get()
    {
        return Ok("HELLO WORLD!");
    }
    
    [HttpPost("traffic")]
    [ProducesResponseType(StatusCodes.Status200OK)]
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
        
        await _networkService.CreateTrafficWindowAsync(trafficWindowDto);
        return Created();
    }
}