package com.example.demo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.util.Random;
import java.util.concurrent.TimeUnit;


@RestController
class SimpleRestController {

  Logger logger = LoggerFactory.getLogger(SimpleRestController.class);

  @GetMapping("/slow")
  String slow() throws InterruptedException{
    int delay = new Random().nextInt(3) + 1;
    TimeUnit.SECONDS.sleep(delay);
    String mockResult = String.format("Slow method call that has random delay: %d seconds", delay);
    logger.info(mockResult);
    return mockResult;
  }

  @GetMapping("/fast")
  String fast() {
    String mockResult = "Freaky fast method call that does nothing";
    logger.info(mockResult);
    return mockResult;
  }

  @ExceptionHandler(InterruptedException.class)
  public String error() {
    return "unknown error";
  }

}