docker pull traefik:v2.5
docker tag traefik us-central1-docker.pkg.dev/solutions-engineering-248511/se-jwilliams-sandbox/traefik:v2.5
docker push us-central1-docker.pkg.dev/solutions-engineering-248511/se-jwilliams-sandbox/traefik:v2.5
kubectl apply -f ./deployment.yaml
kubectl rollout restart deployment haproxy