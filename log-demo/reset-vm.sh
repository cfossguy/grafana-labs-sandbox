gcloud compute ssh 'se-jwilliams-tomcat-vm' --zone us-central1-a -- './apache-tomcat-8.5.75/bin/shutdown.sh'
echo "tomcat stopped"
gcloud compute ssh 'se-jwilliams-tomcat-vm' --zone us-central1-a -- 'sudo rm -rf apache-tomcat-*; sudo rm -rf mylogs'
echo "tomcat deleted"
gcloud compute ssh 'se-jwilliams-tomcat-vm' --zone us-central1-a -- 'sudo rm -rf /usr/bin/grafana-agent'
gcloud compute ssh 'se-jwilliams-tomcat-vm' --zone us-central1-a -- 'sudo rm -rf /usr/bin/grafana-agentctl'
echo "grafana agent deleted"