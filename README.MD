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
cd spring-node
./deploy.sh
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
#### Grafana agent tweaks to capture node_exporter metrics (permissions/mounts)
Refer to "spec" section in [grafana-agent/agent-bare.yml](./grafana-agent/agent-bare.yml). You also need 
to tweak the "agent.yaml |" output to look like:

```
server:
  http_listen_port: 12345
integrations:
  agent:
    enabled: true
  node_exporter:
    enabled: true
    rootfs_path: /host/root
    sysfs_path: /host/sys
    procfs_path: /host/proc
  prometheus:
    wal_directory: /tmp/grafana-agent-wal
    global:
      scrape_interval: 15s
      remote_write:...
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
7.  Import Graphite Carbon Metrics dashboard