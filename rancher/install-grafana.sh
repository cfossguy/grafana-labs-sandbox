kubectl create configmap ge-config --from-file=./grafana.ini
kubectl apply -f ./grafana.yaml
kubectl port-forward service/grafana 3000:3000