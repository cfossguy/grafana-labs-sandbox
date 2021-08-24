ytt -f ./grafana-agent --output-files ./.config
kubectl apply -f ./.config/agent-config-map.yml
kubectl rollout restart deployment grafana-agent
kubectl get pods -w