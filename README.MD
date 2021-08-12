# Command Line Snippets

### Prerequisites
1. Prometheus 2.x.x running locally and added to path
2. OpenJDK to build example spring app
3. Grafana installed locally and added to path

### Prometheus
```
prometheus --config.file=./demo-config/prometheus.yml
```
prometheus will be running on http://localhost:9090

### Grafana
```
cd $GRAFANA_HOME
grafana-server web
```

### Spring Boot Sample 
```
cd spring-node
./mvnw clean package
./mvnw spring-boot:run
```
spring boot app prometheus endpoint http://localhost:8082/actuator/prometheus