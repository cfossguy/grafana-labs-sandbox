./mvnw clean package
./mvnw spring-boot:build-image
docker tag demo:0.0.1-SNAPSHOT williamsjt/spring-node:latest
docker push williamsjt/spring-node:latest
kubectl rollout restart deployment spring-node