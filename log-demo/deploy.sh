mvn clean package
gcloud compute scp ./target/log-demo-1.0-SNAPSHOT.war se-jwilliams-tomcat-vm:~/apache-tomcat-8.5.75/webapps --zone=us-central1-a
gcloud compute scp ./_grafana-agent.yaml se-jwilliams-tomcat-vm:~/grafana-agent.yaml --zone=us-central1-a
