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

  @GetMapping("/fast/{s}")
  String fast(@PathVariable("s") int s)  throws InterruptedException{
    String mockResult = "Fast method call that returns a random length string";
    Random random = new Random();

    int nbr = (random.nextInt(s) + 1) * 100;
    logger.info(mockResult);
    for(int i=0; i<nbr; i++) {
        mockResult = mockResult + "LOL!";
    }
    return mockResult;
  }

  @GetMapping("/slow/{s}")
  String slow(@PathVariable("s") int s) throws InterruptedException{
    String mockResult = "Slow method call that returns a random length string";
    Random random = new Random();
    int nbr = (random.nextInt(s) + 1) * 100;
    logger.warn("About to go to sleep for a bit");
    TimeUnit.MILLISECONDS.sleep(nbr);
    logger.info("Woke up after a brief nap");

    for(int i=0; i<nbr; i++) {
        mockResult = mockResult + "LOL!";
    }

    return mockResult;
  }

  @GetMapping("/roulette/{odds}")
  String roulette(@PathVariable("odds") int odds) throws InterruptedException {
    String response = String.format("You have a 1 in %d chance of NOT getting this message", odds);
    Random random = new Random();
    int nbr = random.nextInt(odds) + 1;

    if (nbr == odds) {
        TimeUnit.SECONDS.sleep(1);
        throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
    }
    logger.warn(response);
    return response;
  }

  @GetMapping("/terminate")
  String terminate() {
    logger.error("Who told you to do that?");
    System.exit(-1);
    return "you will never see this response. i've been terminated";
  }

  @GetMapping("/trip/{count}")
  String trip(@PathVariable("count") int count) {
    String slowSvcUrl = "http://localhost:" + serverPort + "/slow/2";
    String fastSvcUrl = "http://localhost:" + serverPort + "/fast/1";
    String response = "";
    for(int i=0; i<count; i++) {
      response = restTemplate.getForObject(slowSvcUrl, String.class );
      logger.info("Making call to the slow endpoint");

      response = response + restTemplate.getForObject(fastSvcUrl, String.class );
      logger.info("Making call to the fast endpoint");
    }
    logger.warn(String.format("%d round trips to fast and slow services", count));
    return response;
  }

  @ExceptionHandler({InterruptedException.class, ResponseStatusException.class})
  public String error(Exception e) throws Exception {
    logger.error(e.getMessage(), e);
    throw e;
  }

  @Bean
  RestTemplate restTemplate() {
    return new RestTemplate();
  }

}