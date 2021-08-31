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

### Grafana Agent k8s 
1. Run ytt to inject secrets into configs
2. Delete grafana agent deployment
3. Delete grafana agent logs daemonset
4. Apply grafana agent configmap
5. Apply grafana agent logs configmap
6. Deploy grafana agent deployment
7. Deploy grafana agent logs daemonset
8. Watch the pod create/runs
```
./install-agent.sh
```

### Spring Boot on k8s
```
./mvnw clean package
./mvnw spring-boot:build-image
docker tag demo:0.0.1-SNAPSHOT williamsjt/spring-node:latest
docker push williamsjt/spring-node:latest
kubectl apply -f ./spring-node/deployment.yaml
kubectl rollout restart deployment spring-node
kubectl get service spring-node -w 
```

* local - spring boot app prometheus endpoint http://localhost:8082/actuator/prometheus
* local - spring boot app prometheus endpoint http://localhost:8082/fast and http://localhost:8082/slow
* k8s - spring boot app endpoint http://EXTERNAL-IP/fast and http://EXTERNAL-IP/slow

### K6 load test
```
cd k6
k6 run --vus 20 --duration 300s script.js
```

### Magic YAML Snippets
#### prometheus scrape all spring-boot endpoints in k8s cluster
```
scrape_configs:
  - job_name: integrations/spring-boot
    metrics_path: /actuator/prometheus
    kubernetes_sd_configs:
      - role: endpoints
    relabel_configs:
      - source_labels: [ __meta_kubernetes_endpoints_name ]
        target_label: endpoint_name
        action: replace
        replacement: $1
```

### Install Node exporter directly on linux host
``` 
gcloud compute ssh <NODE_NAME> 
cd /var/lib/toolbox
sudo wget https://github.com/prometheus/node_exporter/releases/download/v1.2.2/node_exporter-1.2.2.linux-amd64.tar.gz
sudo tar -xvf /var/lib/toolbox/node_exporter-1.2.2.linux-amd64.tar.gz
./node_exporter
sudo wget https://github.com/prometheus/prometheus/releases/download/v2.29.2/prometheus-2.29.2.linux-amd64.tar.gz
sudo tar -xvf /var/lib/toolbox/prometheus-2.29.2.linux-amd64.tar.gz
sudo mv prometheus-2.29.2.linux-amd64/ prometheus
./prometheus
```