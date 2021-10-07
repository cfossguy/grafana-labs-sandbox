echo making a config directory that should not be checked into source control
mkdir -p .config

echo "INSTALLING BARE METRICS AGENT"
wget -O agent-bare.yaml https://raw.githubusercontent.com/grafana/agent/main/production/kubernetes/agent-bare.yaml
cp agent-bare.yaml ./.config
sed -i '' 's/${NAMESPACE}/YOUR_NAMESPACE/g' .config/agent-bare.yaml
sed -i '' "s/YOUR_NAMESPACE/$YOUR_NAMESPACE/g" .config/agent-bare.yaml
kubectl apply -f .config/agent-bare.yaml

echo "INSTALLING METRICS AGENT CONFIGMAP (CONTAINS SECRETS)"
cp agent-config-map.yaml ./.config
sed -i '' "s/YOUR_CLUSTER_NAME/$YOUR_CLUSTER_NAME/g" .config/agent-config-map.yaml
sed -i '' "s#YOUR_REMOTE_WRITE_URL#$YOUR_REMOTE_WRITE_URL#g" .config/agent-config-map.yaml
sed -i '' "s/YOUR_REMOTE_WRITE_USERNAME/$YOUR_REMOTE_WRITE_USERNAME/g" .config/agent-config-map.yaml
sed -i '' "s/YOUR_REMOTE_WRITE_PASSWORD/$YOUR_REMOTE_WRITE_PASSWORD/g" .config/agent-config-map.yaml
kubectl apply -f .config/agent-config-map.yaml -n $YOUR_NAMESPACE

echo "RESTARTING METRICS GRAFANA AGENT"
kubectl rollout restart deployment/grafana-agent -n $YOUR_NAMESPACE

echo "INSTALLING LOGS BARE AGENT"
wget -O agent-loki.yaml https://raw.githubusercontent.com/grafana/agent/main/production/kubernetes/agent-loki.yaml
cp agent-loki.yaml ./.config
sed -i '' "s/YOUR_NAMESPACE/$YOUR_NAMESPACE/g" .config/agent-loki.yaml
kubectl apply -f .config/agent-loki.yaml -n $YOUR_NAMESPACE

echo "INSTALLING LOGS AGENT CONFIGMAP (CONTAINS SECRETS)"
cp agent-loki-config-map.yaml ./.config
sed -i '' "s/YOUR_NAMESPACE/$YOUR_NAMESPACE/g" .config/agent-loki-config-map.yaml
sed -i '' "s#YOUR_LOKI_ENDPOINT#$YOUR_LOKI_ENDPOINT#g" .config/agent-loki-config-map.yaml
sed -i '' "s/YOUR_LOKI_USERNAME/$YOUR_LOKI_USERNAME/g" .config/agent-loki-config-map.yaml
sed -i '' "s/YOUR_LOKI_PASSWORD/$YOUR_LOKI_PASSWORD/g" .config/agent-loki-config-map.yaml
kubectl apply -f .config/agent-loki-config-map.yaml -n $YOUR_NAMESPACE

echo "RESTARTING LOGS GRAFANA AGENT"
kubectl rollout restart ds/grafana-agent-logs -n $YOUR_NAMESPACE

echo "INSTALLING TRACES AGENT"
wget -O agent-traces.yaml https://raw.githubusercontent.com/grafana/agent/main/production/kubernetes/agent-traces.yaml
cp agent-traces.yaml ./.config
sed -i '' "s/YOUR_NAMESPACE/$YOUR_NAMESPACE/g" .config/agent-traces.yaml
kubectl apply -f .config/agent-traces.yaml -n $YOUR_NAMESPACE

echo "INSTALLING TRACES AGENT CONFIGMAP (CONTAINS SECRETS)"
cp agent-tempo-config-map.yaml ./.config
sed -i '' "s/YOUR_TEMPO_USER/$YOUR_TEMPO_USER/g" .config/agent-tempo-config-map.yaml
sed -i '' "s/YOUR_TEMPO_PASSWORD/$YOUR_TEMPO_PASSWORD/g" .config/agent-tempo-config-map.yaml
sed -i '' "s/YOUR_NAMESPACE/$YOUR_NAMESPACE/g" .config/agent-tempo-config-map.yaml
kubectl apply -f .config/agent-tempo-config-map.yaml -n $YOUR_NAMESPACE

echo "RESTARTING TRACES GRAFANA AGENT"
kubectl rollout restart deployment grafana-agent-traces -n $YOUR_NAMESPACE