./mvnw clean package
./mvnw spring-boot:build-image
docker tag demo:0.0.1-SNAPSHOT us-central1-docker.pkg.dev/solutions-engineering-248511/se-jwilliams-sandbox/spring-node:latest
docker push us-central1-docker.pkg.dev/solutions-engineering-248511/se-jwilliams-sandbox/spring-node:latest
kubectl apply -f ./deployment.yaml
kubectl rollout restart deployment spring-node