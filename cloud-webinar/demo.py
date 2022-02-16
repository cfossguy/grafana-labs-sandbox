# importing the required modules
import click
import os
import requests
import yaml
import webbrowser
from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)
gcp_vm_name = os.getenv('gcp_vm_name')
gcp_project = os.getenv('gcp_project')
gcp_zone = os.getenv('gcp_zone')
gcp_machine_type = os.getenv('gcp_machine_type')
gcp_service_account = os.getenv('gcp_service_account')

@click.group()
def cli():
    pass

@click.command()
def install_vm():
    """Provision a Linux VM on GCP."""
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
                       "image=projects/ubuntu-os-cloud/global/images/ubuntu-1804-bionic-v20220131,mode=rw,size=10," \
                       f"type=projects/{gcp_project}/zones/{gcp_zone}/diskTypes/pd-balanced " \
                       "--no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any"



    os.system(gcloud_create)
    print("VM provisioned on GCP. Wait ~60 seconds.")
    print("Next run: ./demo 2.install-node")

@click.command()
def install_node():
    """Provision Node on Linux VM."""
    install_node = "curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash - ;" \
                   "sudo apt-get install -y nodejs; " \
                   "npm install express --save; " \
                   "npm install prom-client --save; " \
                   "sudo npm install nodemon -g"

    os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- '{install_node}'")
    print("Node + express and prom-client modules installed on VM. Run Next: ./demo 3.install-node-app")

@click.command()
def install_node_app():
    """Provision node sample app to VM."""
    os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- 'mkdir -p ./node-app'")
    print("Created node-app directory")
    os.system(f"gcloud compute scp ./node-app/app.mjs {gcp_vm_name}:~/node-app --zone={gcp_zone}")
    start_node = "nodemon ./node-app/app.mjs"
    os.system(f"nohup gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- '{start_node}' &>/dev/null &")
    #os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- '{start_node}'")
    print("Node running in background")

@click.command()
def ssh():
    """SSH into the Linux VM. (Troubleshooting)"""
    os.system(f"gcloud beta compute ssh --zone '{gcp_zone}' '{gcp_vm_name}' --tunnel-through-iap")

@click.command()
def teardown():
    """Un-provision Linux VM on GCP."""
    os.system(f"gcloud compute instances delete {gcp_vm_name} --zone={gcp_zone} --quiet")
    print(f"{gcp_vm_name} VM in {gcp_zone} has been deleted")

cli.add_command(install_vm, name="1.install-vm")
cli.add_command(install_node, name="2.install-node")
cli.add_command(install_node_app, name="3.install-node-app")
cli.add_command(teardown, name="teardown")
cli.add_command(ssh, name="ssh")

if __name__ == "__main__":
    cli()
