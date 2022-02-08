# importing the required modules
import click
import os
import time
import subprocess
import requests
import yaml
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
    print("VM provisioned on GCP. Wait ~60 seconds. Next run: ./demo 2.install-dependencies")

@click.command()
def install_dependencies():
    """Provision OpenJDK+Maven+Tomcat on Linux VM."""
    install_dependencies = "sudo apt-get -qq install default-jdk; sudo apt-get -qq install unzip; " \
                     "sudo wget -nc https://dlcdn.apache.org/maven/maven-3/3.8.4/binaries/apache-maven-3.8.4-bin.zip; " \
                     "sudo unzip -o apache-maven-*-bin.zip; " \
                     "sudo wget -nc https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.75/bin/apache-tomcat-8.5.75.zip; " \
                     "sudo unzip -o apache-tomcat-*.zip; " \
                     "sudo chmod 755 -R ./apache-*/; " \
                     "sudo chown -R `whoami`:`whoami` ./apache-tomcat-8.5.75"

    start_tomcat = "./apache-tomcat-8.5.75/bin/startup.sh"

    os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- '{install_dependencies}'")
    print("OpenJDK, Apache Maven and Apache Tomcat downloaded and installed")
    os.system(f"nohup gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- '{start_tomcat}' &>/dev/null &")
    print("Tomcat started in background on VM. Run Next: ./demo 3.install-app")

@click.command()
def install_app():
    """Provision log-demo sample app to Tomcat."""
    os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- 'mkdir -p ./log-demo'")
    print("Created log-demo directory")
    os.system(f"gcloud compute scp ./pom.xml {gcp_vm_name}:~/log-demo --zone={gcp_zone}")
    print("Copied pom.xml to log-demo directory")
    os.system(f"gcloud compute scp --recurse ./src {gcp_vm_name}:~/log-demo --zone={gcp_zone}")
    print("Copied source files to log-demo directory")
    os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- './apache-maven-3.8.4/bin/mvn clean package -f ./log-demo/pom.xml;"
              f"cp ./log-demo/target/log-demo-*.war ./apache-tomcat-*/webapps'")
    print("WAR file built and deployed to tomcat webapps directory")
    print("Run Next: ./demo 4.test-app")

@click.command()
def test_app():
    """Invoke the log-demo sample application"""
    external_ip = subprocess.check_output(
        ["gcloud", "compute", "instances", "list", f"--filter=name={gcp_vm_name}", "--format=value(EXTERNAL_IP)"])
    external_ip = external_ip.strip().decode("utf-8")
    test_times = 10
    sleep_duration = 1
    print(f"Application should be available at: http://{external_ip}:8080/log-demo-1.0-SNAPSHOT/")
    for x in range(test_times):
        test_url = f"http://{external_ip}:8080/log-demo-1.0-SNAPSHOT/"
        test_response = requests.get(test_url)
        print(test_response.text)
        print(f"Invoked test url {x+1} of {test_times} times to generate log entries")
    print("Run Next: ./demo 5.install-grafana-agent")

@click.command()
def install_grafana_agent():
    """Provision grafana agent on Linux VM."""
    downlod_grafana_agent = "sudo wget -nc https://github.com/grafana/agent/releases/download/v0.22.0/agent-linux-amd64.zip; " \
                            "unzip -o agent-linux-amd64.zip; chmod a+x agent-linux-amd64;"
    os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- '{downlod_grafana_agent}'")
    print("Grafana agent installed")
    print("Run Next: ./demo 6.set-agent-config-and-run")

@click.command()
def ssh():
    """SSH into the Linux VM. (Troubleshooting)"""
    os.system(f"gcloud beta compute ssh --zone '{gcp_zone}' '{gcp_vm_name}' --tunnel-through-iap")

@click.command()
def set_grafana_agent_config_and_run():
    """Apply grafana cloud credentials to a metrics + logs grafana agent configuration."""
    gcloud_username_metrics = os.getenv('gcloud_username_metrics')
    gcloud_username_logs = os.getenv('gcloud_username_logs')
    gcloud_password_metrics = os.getenv('gcloud_password_metrics')
    gcloud_password_logs = os.getenv('gcloud_password_logs')
    gcloud_remote_write_url_metrics = os.getenv('gcloud_remote_write_url_metrics')
    gcloud_remote_write_url_logs = os.getenv('gcloud_remote_write_url_logs')

    os.makedirs(os.path.dirname("./.config/"), exist_ok=True)

    with open(r'./grafana-agent-template.yaml') as file:
        contents = yaml.load(file, Loader=yaml.FullLoader)
    with open(r'./.config/grafana-agent.yaml', 'w') as file:
        contents['metrics']['global']['remote_write'][0]['basic_auth']['password'] = gcloud_password_metrics
        contents['metrics']['global']['remote_write'][0]['basic_auth']['username'] = gcloud_username_metrics
        contents['metrics']['global']['remote_write'][0]['url'] = gcloud_remote_write_url_metrics

        contents['logs']['configs'][0]['clients'][0]['basic_auth']['password'] = gcloud_password_logs
        contents['logs']['configs'][0]['clients'][0]['basic_auth']['username'] = gcloud_username_logs
        contents['logs']['configs'][0]['clients'][0]['url'] = gcloud_remote_write_url_logs
        yaml.dump(contents, file)
    print("A new grafana agent configuration is available in - '.config' folder")
    print("WARNING - Files written to .config directory should not be checked into source control because they contain secrets!")
    os.system(f"gcloud compute scp './.config/grafana-agent.yaml' {gcp_vm_name}:'~/grafana-agent.yaml' --zone={gcp_zone}")
    print("Grafana agent configuration copied to VM")
    os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- './agent-linux-amd64 -config.file ./grafana-agent.yaml'")

@click.command()
def teardown():
    """Un-provision Linux VM on GCP."""
    os.system(f"gcloud compute instances delete {gcp_vm_name} --zone={gcp_zone} --quiet")
    print(f"{gcp_vm_name} VM in {gcp_zone} has been deleted")

cli.add_command(install_vm, name="1.install-vm")
cli.add_command(install_dependencies, name="2.install-dependencies")
cli.add_command(install_app, name="3.install-app")
cli.add_command(test_app, name="4.test-app")
cli.add_command(install_grafana_agent, name="5.install-grafana-agent")
cli.add_command(set_grafana_agent_config_and_run, name="6.set-agent-config-and-run")
cli.add_command(teardown, name="teardown")
cli.add_command(ssh, name="ssh")

if __name__ == "__main__":
    cli()
