using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace WebApplication.Controllers
{
    [ApiController]
    public class SimpleRestController : ControllerBase
    {
        private readonly ILogger<SimpleRestController> _logger;

        public SimpleRestController(ILogger<SimpleRestController> logger)
        {
            _logger = logger;
        }
        
        [Route("Fast")] 
        [HttpGet] 
        public string Fast(int k)
        {
            _logger.LogInformation("Fast method call that returns a fixed length string");
            return getMockResponse(k);
        }
        
        [Route("HelloWorld/Welcome")] 
        [HttpGet] 
        public string Welcome()
        {
            return "This is the Welcome action method...";
        }
        
        private string getMockResponse(int s) {
            string response = "";
            int kbSize = s * 1000;

            for(int i=0; i<kbSize; i++) {
                if (i % 100 == 0)
                    response += "\n";
                response += "!";
            }

            return response;
        }
    }
}