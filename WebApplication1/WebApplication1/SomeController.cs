using Microsoft.AspNetCore.Mvc;

namespace WebApplication1;

public class SomeController : Controller
{
    // GET
    public IActionResult Index()
    {
        return View();
    }
}