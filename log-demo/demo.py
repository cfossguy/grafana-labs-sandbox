# importing the required modules
import time

import click
import os
from dotenv import load_dotenv

load_dotenv(override=True)
gcp_vm_name = os.getenv('gcp_vm_name')
gcp_project = os.getenv('gcp_project')
gcp_zone = os.getenv('gcp_zone')
gcp_machine_type = os.getenv('gcp_machine_type')
gcp_service_account = os.getenv('gcp_service_account')

@click.group()
def cli():
    pass

@click.command('provision_vm')
def provision_vm():
    gcloud_create = f"gcloud compute instances create {gcp_vm_name} --project={gcp_project} " \
                       f"--zone={gcp_zone} --machine-type={gcp_machine_type} " \
                       "--network-interface=network-tier=PREMIUM,subnet=default --metadata=enable-oslogin=true " \
                       f"--maintenance-policy=MIGRATE --service-account={gcp_service_account}" \
                       " --scopes=https://www.googleapis.com/auth/devstorage.read_only," \
                       "https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write," \
                       "https://www.googleapis.com/auth/servicecontrol," \
                       "https://www.googleapis.com/auth/service.management.readonly," \
                       "https://www.googleapis.com/auth/trace.append --tags=http-server,https-server" \
                       " --create-disk=auto-delete=yes,boot=yes,device-name=instance-1," \
                       "image=projects/ubuntu-os-cloud/global/images/ubuntu-1804-bionic-v20220118,mode=rw,size=10," \
                       f"type=projects/{gcp_project}/zones/{gcp_zone}/diskTypes/pd-balanced " \
                       "--no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any"

    os.system(gcloud_create)
    print("VM provisioned on GCP")

@click.command('provision_tomcat')
def provision_tomcat():
    install_dependencies = "sudo apt-get -qq install default-jdk; sudo apt-get -qq install unzip; " \
                     "sudo wget -nc https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.75/bin/apache-tomcat-8.5.75.zip; " \
                     "sudo unzip apache-tomcat-*.zip; " \
                     "sudo chmod 755 -R ./apache-tomcat-8.5.75/; " \
                     "sudo chown -R `whoami`:`whoami` ~/apache-tomcat-8.5.75"

    start_tomcat = "nohup ~/apache-tomcat-8.5.75/bin/startup.sh"

    os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- '{install_dependencies};{start_tomcat}'")
    print("Tomcat installed and started on VM")

@click.command('provision_grafana_agent')
def provision_grafana_agent():

    install_grafana_agent = "sudo wget -nc https://github.com/grafana/agent/releases/download/v0.22.0/agent-linux-amd64.zip; " \
                            "unzip agent-linux-amd64.zip; chmod a+x agent-linux-amd64;" \
                            "sudo ./agent-linux-amd64 -config.file ./grafana-agent.yaml"

    os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- '{install_grafana_agent}'")

@click.command()
def teardown():
    print("teardown")

cli.add_command(provision_vm)
cli.add_command(provision_tomcat)
cli.add_command(provision_grafana_agent)

if __name__ == "__main__":
    cli()
