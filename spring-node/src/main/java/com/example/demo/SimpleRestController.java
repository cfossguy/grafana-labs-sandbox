package com.example.demo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.client.RestTemplate;
import java.util.concurrent.TimeUnit;

@RestController
class SimpleRestController {

  Logger logger = LoggerFactory.getLogger(SimpleRestController.class);

  @Value( "${server.port}" )
  private String serverPort;

  @Autowired
  RestTemplate restTemplate;

  @GetMapping("/fast")
  String fast() {
    String mockResult = "Freaky fast method call that does nothing";
    logger.info(mockResult);
    return mockResult;
  }

  @GetMapping("/slow")
  String slow() throws InterruptedException{
    String googleSvcUrl = "http://localhost:" + serverPort + "/google";
    String googleResponse = restTemplate.getForObject(googleSvcUrl, String.class );
    logger.info(String.format("Google response length: %d", googleResponse.length()));
    logger.info("About to go to sleep for 1 second");
    TimeUnit.SECONDS.sleep(1);
    logger.info("Woke up after a brief nap");
    String fastSvcUrl = "http://localhost:" + serverPort + "/fast";
    String fastResponse = restTemplate.getForObject(fastSvcUrl, String.class );
    return "slow method call that slept for 1 second";
  }

  @GetMapping("/google")
  String google() {
    String response = restTemplate.getForObject("http://google.com", String.class );
    logger.info(String.format("Google response payload size: %d", response.length()));
    return response;
  }

  @GetMapping("/trip/{count}")
  String trip(@PathVariable("count") int count) {
    String slowSvcUrl = "http://localhost:" + serverPort + "/slow";
    for(int i=0; i<count; i++) {
      String response = restTemplate.getForObject(slowSvcUrl, String.class );
      logger.info(String.format("Microservice response: %s", response));
    }
    String mockResult = String.format("%d round trips to /slow", count);
    logger.info(mockResult);
    return mockResult;
  }

  @ExceptionHandler(InterruptedException.class)
  public String error() {
    return "unknown error";
  }

  @Bean
  RestTemplate restTemplate() {
    return new RestTemplate();
  }

}