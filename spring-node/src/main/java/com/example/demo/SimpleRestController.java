package com.example.demo;

import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.ExceptionHandler;
import java.util.concurrent.TimeUnit;
import java.lang.InterruptedException;
import java.util.Random;

@RestController
class SimpleRestController {

  @GetMapping("/slow")
  String slow() throws InterruptedException{
    int delay = new Random().nextInt(3) + 1;
    TimeUnit.SECONDS.sleep(delay);
    return String.format("Delay of %d seconds", delay);
  }

  @GetMapping("/fast")
  String fast() {
    return "that was sooo fast";
  }

  @ExceptionHandler(InterruptedException.class)
  public String error() {
    return "unknown error";
  }

}