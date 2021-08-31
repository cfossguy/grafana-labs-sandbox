package com.example.demo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.server.ResponseStatusException;

import java.util.Random;
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
    Random random = new Random();
    int nbr = random.nextInt(2) + 1;
    logger.info(String.format("About to go to sleep for %d second", nbr));
    TimeUnit.SECONDS.sleep(nbr);
    logger.info("Woke up after a brief nap");

    return String.format("About to go to sleep for %d second", nbr);
  }

  @GetMapping("/roulette")
  String roulette() {
    String response = "You have a 1 in 100 chance of NOT getting this message.";
    Random random = new Random();
    int nbr = random.nextInt(100) + 1;
    if (nbr == 100) {
        logger.error("Something very bad just happened.");
        throw new ResponseStatusException(
                HttpStatus.INTERNAL_SERVER_ERROR);
    }
    logger.info(response);
    return response;
  }

  @GetMapping("/trip/{count}")
  String trip(@PathVariable("count") int count) {
    String slowSvcUrl = "http://localhost:" + serverPort + "/slow";
    String fastSvcUrl = "http://localhost:" + serverPort + "/fast";

    for(int i=0; i<count; i++) {
      String response = restTemplate.getForObject(slowSvcUrl, String.class );
      logger.info(String.format("Microservice response: %s", response));

      response = restTemplate.getForObject(fastSvcUrl, String.class );
      logger.info(String.format("Microservice response: %s", response));
    }
    String mockResult = String.format("%d round trips to multiple services", count);
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