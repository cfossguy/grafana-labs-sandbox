using Microsoft.AspNetCore.Mvc;

namespace WebApplication.Controllers
{
    [ApiController]
    public class HelloWorldController : ControllerBase
    {
        [Route("HelloWorld")] 
        [HttpGet] 
        public string Index()
        {
            return "This is my default action...";
        }
        
        [Route("HelloWorld/Welcome")] 
        [HttpGet] 
        public string Welcome()
        {
            return "This is the Welcome action method...";
        }
    }
}