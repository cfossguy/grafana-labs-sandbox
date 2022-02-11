# importing the required modules
import click
import os
import requests
import yaml
import webbrowser
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
    print("VM provisioned on GCP. Wait ~60 seconds.")
    print("Next run: ./demo 2.install-dependencies")

@click.command()
def install_dependencies():
    """Provision OpenJDK+Maven+Tomcat+K6+Grafana Agent on Linux VM."""
    install_dependencies = "sudo apt-get -qq install default-jdk; sudo apt-get -qq install unzip; " \
                     "sudo wget -nc https://dlcdn.apache.org/maven/maven-3/3.8.4/binaries/apache-maven-3.8.4-bin.zip; " \
                     "sudo unzip -o apache-maven-*-bin.zip; " \
                     "sudo wget -nc https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.75/bin/apache-tomcat-8.5.75.zip; " \
                     "sudo unzip -o apache-tomcat-*.zip; " \
                     "sudo chmod 755 -R ./apache-*/; " \
                     "sudo chown -R `whoami`:`whoami` ./apache-tomcat-8.5.75; " \
                     "sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69; " \
                     "echo \"deb https://dl.k6.io/deb stable main\" | sudo tee /etc/apt/sources.list.d/k6.list; " \
                     "sudo apt-get update; " \
                     "sudo apt-get install k6; " \
                     "sudo wget -nc https://github.com/grafana/agent/releases/download/v0.22.0/agent-linux-amd64.zip; " \
                     "unzip -o agent-linux-amd64.zip; chmod a+x agent-linux-amd64;"

    os.system(f"gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- '{install_dependencies}'")
    print("OpenJDK, Maven, Tomcat and K6 downloaded and installed")
    start_tomcat = "./apache-tomcat-8.5.75/bin/startup.sh"
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
    print("Run Next: ./demo 4.load-test-app")

@click.command()
def load_test_app():
    """Run k6 load test"""
    run_k6 = "k6 run k6-script.js --quiet"
    os.system(f"gcloud compute scp k6-script.js {gcp_vm_name}:~/ --zone={gcp_zone}")
    os.system(f"nohup gcloud compute ssh --zone {gcp_zone} {gcp_vm_name} -- '{run_k6}' &>/dev/null &")
    print("Load test will run in background for 24 hours")
    print("Run Next: ./demo 5.install-dashboard")

@click.command()
def install_dashboard():
    """Provision a custom metrics+logs"""
    gcloud_password_dashboards = os.getenv('gcloud_password_dashboards')
    gcloud_domain_dashboards = os.getenv('gcloud_domain_dashboards')
    url = f"{gcloud_domain_dashboards}/api/dashboards/db"

    dashboard = open('dashboard.json')
    headers = {"Accept": "application/json",
               "Content-Type": "application/json",
               "Authorization": f"Bearer {gcloud_password_dashboards}"}
    response = requests.post(url=url, data=dashboard, headers=headers)
    try:
        dashboard_url = f"{gcloud_domain_dashboards}{response.json()['url']}"
        print(f"Dashboard url is:{dashboard_url}")
        webbrowser.open(dashboard_url)
    except KeyError:
        print(f"Error occurred: {response.text}")
    print("Run Next: ./demo 6.set-agent-config-and-run")

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
def ssh():
    """SSH into the Linux VM. (Troubleshooting)"""
    os.system(f"gcloud beta compute ssh --zone '{gcp_zone}' '{gcp_vm_name}' --tunnel-through-iap")

@click.command()
def teardown():
    """Un-provision Linux VM on GCP."""
    os.system(f"gcloud compute instances delete {gcp_vm_name} --zone={gcp_zone} --quiet")
    print(f"{gcp_vm_name} VM in {gcp_zone} has been deleted")

cli.add_command(install_vm, name="1.install-vm")
cli.add_command(install_dependencies, name="2.install-dependencies")
cli.add_command(install_app, name="3.install-app")
cli.add_command(load_test_app, name="4.load-test-app")
cli.add_command(install_dashboard, name="5.install-dashboard")
cli.add_command(set_grafana_agent_config_and_run, name="6.set-agent-config-and-run")
cli.add_command(teardown, name="teardown")
cli.add_command(ssh, name="ssh")

if __name__ == "__main__":
    cli()
