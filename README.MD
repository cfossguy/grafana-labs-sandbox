# Command Line Snippets

### Prometheus
```
cd prometheus-2.29.1
prometheus --config.file=../demo-config/prometheus.yml
```
prometheus will be running on http://localhost:9090

### Spring Boot Sample 
```
cd spring-node
mvnw clean package
mvnw spring-boot:run
```
spring boot app prometheus endpoint http://localhost:8082/actuator/prometheus