echo "INSTALLING BARE METRICS AGENT"
wget -O agent-bare.yaml https://raw.githubusercontent.com/grafana/agent/main/production/kubernetes/agent-bare.yaml
sed -i '' 's/${NAMESPACE}/grafana/g' agent-bare.yaml
kubectl apply -f ./agent-bare.yaml

echo "INSTALLING METRICS AGENT CONFIGMAP (CONTAINS SECRETS)"
kubectl apply -f ./_agent-config-map.yaml -n grafana

echo "RESTARTING METRICS GRAFANA AGENT"
kubectl rollout restart deployment/grafana-agent -n grafana

echo "INSTALLING LOGS BARE AGENT"
wget -O agent-loki.yaml https://raw.githubusercontent.com/grafana/agent/main/production/kubernetes/agent-loki.yaml
sed -i '' 's/YOUR_NAMESPACE/grafana/g' agent-loki.yaml
kubectl apply -f ./agent-loki.yaml

echo "INSTALLING LOGS AGENT CONFIGMAP (CONTAINS SECRETS)"
kubectl apply -f ./_agent-loki-config-map.yaml -n grafana

echo "RESTARTING LOGS GRAFANA AGENT"
kubectl rollout restart ds/grafana-agent-logs -n grafana

echo "INSTALLING TRACES AGENT"
wget -O agent-traces.yaml https://raw.githubusercontent.com/grafana/agent/main/production/kubernetes/agent-traces.yaml
sed -i '' 's/YOUR_NAMESPACE/grafana/g' agent-traces.yaml
kubectl apply -f ./agent-traces.yaml -n grafana

echo "INSTALLING TRACES AGENT CONFIGMAP (CONTAINS SECRETS)"
kubectl apply -f ./_agent-tempo-config-map.yaml -n grafana

echo "RESTARTING TRACES GRAFANA AGENT"
kubectl rollout restart deployment grafana-agent-traces -n grafana