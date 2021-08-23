# Command Line Snippets

### Prerequisites
1. YTT installed to manage YAML configuration templates
2. Prometheus 2.x.x running locally and added to path
3. OpenJDK to build example spring app
4. Grafana installed locally and added to path
5. k6 to run load tests on sample application
6. Grafana Cloud account to bounce metrics from local prometheus to the cloud
7. kubectl installed and configured to use a k8s env with RBAC enabled
8. Docker - for building the spring-node image

### Prometheus
```
ytt -f ./prometheus-local --output-files ./.config
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

### Grafana AGent k8s
```
ytt -f ./grafana-agent --output-files ./.config
kubectl apply -f ./.config/agent-config-map.yml
kubectl apply -f ./.config/agent-bare.yml
kubectl rollout restart deployment/grafana-agent
```

### Spring Boot on k8s
```
./mvnw spring-boot:build-image
docker tag demo:0.0.1-SNAPSHOT williamsjt/spring-node:0.0.2
docker push williamsjt/spring-node:0.0.2
kubectl apply -f ./spring-node/deployment.yaml
kubectl get service spring-node -w 
```

* local - spring boot app prometheus endpoint http://localhost:8082/actuator/prometheus
* local - spring boot app prometheus endpoint http://localhost:8082/fast and http://localhost:8082/slow...
* k8s - spring boot app endpoint http://EXTERNAL-IP/fast and http://EXTERNAL-IP/slow...

### K6 load test
```
cd k6
k6 run --vus 10 --duration 300s script.js
```