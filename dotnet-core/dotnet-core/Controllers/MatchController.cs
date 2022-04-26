using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace dotnet_core.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class MatchController : ControllerBase
    {

        private readonly ILogger<MatchController> _logger;

        public MatchController(ILogger<MatchController> logger)
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