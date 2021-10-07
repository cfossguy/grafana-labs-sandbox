# Command Line Snippets

### Easy Start - Grafana Cloud Agent
1. Install "Kubernetes" - grafana agent (metrics) - https://grafana.com/docs/grafana-cloud/quickstart/agent-k8s/k8s_agent_metrics/
2. Install "Kubernetes" - grafana loki agent (logs) - https://grafana.com/docs/grafana-cloud/quickstart/agent-k8s/k8s_agent_logs/
3. Install "Kubernetes" - grafana tempo agent (traces) - https://grafana.com/docs/grafana-cloud/quickstart/agent-k8s/k8s_agent_traces/

The Grafana Agent install is straightforward but it involves:
1. Downloading bare deployment yaml files from github
2. Copy/paste starter configmap files from grafana quickstart guides
3. Replace config map variable placeholders with your environment info(username, password, remote_write...)

### Super Easy Start - Grafana Cloud Agent
You can do a "clean" metrics/logs/traces agent installation on k8s by setting environment variables 
and doing a few find/replaces on the bare deployment files and config map files. This repo contains config map 
files that were copy/pasted from the grafana quickstart guides as/is. 

1. Create "./grafana-agent/.env" file and make sure the following properties are set
```
export YOUR_NAMESPACE=TODO

#grafana metrics agent properties
export YOUR_REMOTE_WRITE_URL=TODO
export YOUR_REMOTE_WRITE_USERNAME=TODO
export YOUR_REMOTE_WRITE_PASSWORD=TODO
export YOUR_CLUSTER_NAME=TODO

#grafana log agent properties
export YOUR_LOKI_ENDPOINT=TODO
export YOUR_LOKI_USERNAME=TODO
export YOUR_LOKI_PASSWORD=TODO

#grafana traces agent properties
export YOUR_TEMPO_USER=TODO
export YOUR_TEMPO_PASSWORD=TODO
```
2. Source the environment variables into your shell session and run the wrapper deploy shell script. 
This will create YAML files that can be applied to your k8s cluster. 
```
cd ./grafana-agent
source .env
./deploy.sh
kubectl get pods -n $YOUR_NAMESPACE
```
3. If you see grafana-agent and grafana-agent-logs and grafana-agent-traces pods running, and data in grafana, all is well.

### Prerequisites - local setup
1. YTT installed to manage YAML configuration templates
2. Prometheus 2.x.x running locally and added to path
3. OpenJDK to build example spring app
4. Grafana installed locally and added to path
5. k6 to run load tests on sample application
6. Grafana Cloud account to bounce metrics from local prometheus to the cloud
7. kubectl installed and configured to use a k8s env with RBAC enabled
8. Docker - for building the spring-node image
9. Docker repository - for pulling spring-node image from container registry (demo uses GCP Artifact Registry)

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
./mvnw spring-boot:run
```

### Spring Boot on k8s
```
cd spring-node
./deploy.sh
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

### Scale k8s replicas - Spring Boot
```
kubectl scale deployment spring-node --replicas=6
```

* local - spring boot app prometheus endpoint http://localhost:8082/actuator/prometheus
* local - spring boot app prometheus endpoint http://localhost:8082/fast and http://localhost:8082/slow
* k8s - spring boot app endpoint http://EXTERNAL-IP/fast and http://EXTERNAL-IP/slow

### K6 load test
```
cd k6
k6 run --vus 10 --duration 300s script.js
```

### k8s deploy of k6 scripts
```
cd k6
./deploy.sh
```

### Install Node exporter directly on linux host
#### Do the following in GCP or equivalent cloud/on-prem server
``` 
gcloud compute ssh <NODE_NAME> 
sudo wget https://github.com/prometheus/node_exporter/releases/download/v1.2.2/node_exporter-1.2.2.linux-amd64.tar.gz
sudo tar -xvf node_exporter-1.2.2.linux-amd64.tar.gz
cd node_exporter-1.2.2.linux-amd64
./node_exporter &
sudo wget https://github.com/prometheus/prometheus/releases/download/v2.29.2/prometheus-2.29.2.linux-amd64.tar.gz
sudo tar -xvf prometheus-2.29.2.linux-amd64.tar.gz
cd prometheus-2.29.2.linux-amd64
./prometheus --config.file=prometheus.yml &
```
#### Do the following in local sandbox 
ytt -f ./prometheus-local --output-files ./.config
scp ./.config/prometheus-wordpress.yml to PROMETHEUS_HOME

### Install Promtail(OSS logging agent) on linux host
``` 
gcloud compute ssh <NODE_NAME> 
https://github.com/grafana/loki/releases/download/v2.3.0/promtail-linux-amd64.zip
sudo unzip promtail-linux-amd64.zip
sudo chown USER:GROUP promtail-linux-amd64
./promtail-linux-amd64 
```
#### Log Browser Pattern Match Snippet
Apache Web Server
```
{host="HOSTNAME",job="JOB"} | pattern `<IP> - - <ts> "<method> <uri> <_>" <status> <bytes> "<_>" "<client> <_>"` | method="GET" | method="GET"
sum by (method, status) (rate({host="HOSTNAME",job="JOB"} | pattern `<IP> - - <ts> "<method> <uri> <_>" <status> <bytes> "<_>" "<client> <_>"`[$__interval]))
```

#### Run Graphite in Docker & connect to Grafana 
```
docker run -d --name graphite -p 80:80 -p 8080:8080 -p 2003-2004:2003-2004 -p 2023-2024:2023-2024 -p 8125:8125/udp -p 8126:8126 graphiteapp/graphite-statsd
```

1. Connect Grafana to Graphite - browse to http://localhost:3000 and log in with admin/admin
2. Add Data Source
3. Get Graphite container IP - docker inspect <container-id> | grep -i ipaddr
4. URL: http://localhost:8080
5. Save and Test
6. Click on Dashboards tab (next to Settings tab)
7. Import Graphite Carbon Metrics dashboard