ytt -f ./grafana-agent --output-files ./.config
kubectl delete deployment grafana-agent
kubectl delete ds grafana-agent-logs
kubectl apply -f ./.config/agent-config-map.yml
kubectl apply -f ./.config/agent-bare.yml
kubectl apply -f ./.config/agent-loki-config-map.yml
kubectl apply -f ./.config/agent-loki.yml
kubectl apply -f ./.config/agent-tempo-configmap.yml
kubectl apply -f ./.config/agent-tempo.yml
kubectl get pods -w