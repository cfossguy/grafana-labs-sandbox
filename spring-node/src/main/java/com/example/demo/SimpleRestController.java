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
import org.springframework.web.method.annotation.MethodArgumentTypeMismatchException;
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

  @GetMapping("/fast/{k}")
  String fast(@PathVariable("k") String k) {
    int kbSize = 0;
    try {
        kbSize = Integer.parseInt(k);
    }
    catch (Exception e){
         logger.error(String.format("Invalid API Request Parameter k=%s",k));
         throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
    }

    logger.info("Fast method call that returns a fixed length string");
    return getMockResponse(kbSize);
  }

  @GetMapping("/slow/{s}/{k}")
  String slow(@PathVariable("s") String s, @PathVariable("k") String k) throws InterruptedException {
    int kbSize = 0;
    int sleepTime = 0;
    try {
        kbSize = Integer.parseInt(k);
        sleepTime = Integer.parseInt(s);
    }
    catch (Exception e){
         logger.error(String.format("Invalid API Request Parameter k=%s, s=%s",k,s));
         throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
    }

    logger.warn("About to go to sleep for a bit");
    TimeUnit.SECONDS.sleep(sleepTime);
    logger.info("Woke up after a brief nap");
    return getMockResponse(kbSize);
  }

  @GetMapping("/roulette/{o}")
  String roulette(@PathVariable("o") String o) throws InterruptedException {
    int odds = 0;
    try {
        odds = Integer.parseInt(o);
    }
    catch (Exception e){
         logger.error(String.format("Invalid API Request Parameter o=%s",o));
         throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
    }

    Random random = new Random();
    int nbr = random.nextInt(odds) + 1;
    if (nbr == odds) {
        throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
    }
    logger.warn(String.format("You have a 1 in %d chance of NOT getting this message", odds));
    return getMockResponse(1);
  }

  @GetMapping("/terminate")
  String terminate() {
    logger.error("Who told you to do that?");
    System.exit(-1);
    return "you will never see this response. i've been terminated";
  }

  @GetMapping("/trip/{c}/{s}/{k}")
  String trip(@PathVariable("c") String c, @PathVariable("s") String s, @PathVariable("k") String k) {

    int count = 0;
    int kbSize = 0;
    int sleepTime = 0;

    try {
        count = Integer.parseInt(c);
        kbSize = Integer.parseInt(k);
        sleepTime = Integer.parseInt(s);
    }
    catch (Exception e){
         logger.error(String.format("Invalid API Request Parameter c=%s,s=%s,k=%s",c,s,k));
         throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
    }

    String slowSvcUrl = String.format("http://localhost:%s/slow/%d/%d", serverPort, sleepTime, kbSize);
    String fastSvcUrl = String.format("http://localhost:%s/fast/%d", serverPort, kbSize);
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

  private String getMockResponse(int s) {
    String response = "";
    int kbSize = s * 1000;

    for(int i=0; i<kbSize; i++) {
        if (i % 100 == 0)
            response += "\n";
        response += "!";
    }

    return response;
  }

  @ExceptionHandler({InterruptedException.class})
  public String error(Exception e) throws ResponseStatusException {
    logger.error(e.getMessage(), e);
    throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
  }

  @ExceptionHandler({MethodArgumentTypeMismatchException.class})
  public String errorInvalidInput(Exception e) throws ResponseStatusException {
    logger.error(e.getMessage(), e);
    throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
  }

  @Bean
  RestTemplate restTemplate() {
    return new RestTemplate();
  }

}