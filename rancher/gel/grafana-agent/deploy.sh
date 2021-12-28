echo making a config directory that should not be checked into source control
mkdir -p ./.config

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