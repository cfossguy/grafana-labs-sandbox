# Command Line Snippets

### Prerequisites
1. YTT installed to manage YAML configuration templates
2. Prometheus 2.x.x running locally and added to path
3. OpenJDK to build example spring app
4. Grafana installed locally and added to path
5. k6 to run load tests on sample application
6. Grafana Cloud account to bounce metrics from local prometheus to the cloud

### Prometheus
```
ytt -f ./config --output-files ./.config
prometheus --config.file=./.config/prometheus.yml
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

### K6 load test
```
cd k6
k6 run --vus 10 --duration 30s script.js
```