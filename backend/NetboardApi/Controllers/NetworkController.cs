using Microsoft.AspNetCore.Mvc;

namespace NetboardApi.Controllers;

[ApiController]
[Route("[controller]")]
public class NetworkController : ControllerBase
{
    private readonly ILogger<NetworkController> _logger;

    public NetworkController(ILogger<NetworkController> logger)
    {
        _logger = logger;
    }
    
    [HttpGet]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public IActionResult Get()
    {
        return Ok("HELLO WORLD!");
    }
    
    [HttpPost]
    public IActionResult Post()
    {
        return Ok("HELLO WORLD!");
    }
}