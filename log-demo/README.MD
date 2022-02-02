# Log Demo Guide
This demo is an **infrastructure as code** walk-thru for configuring a 
grafana agent to collect metrics and logs for a legacy tomcat application.
This demo guide is designed for usage with Google Cloud. 

You will not need to edit any Java code. All source code and configuration files and build
scripts/tools are included in this guide so that you can edit the code or configuration. 

## Prerequisites
* Google Cloud's [SDK](https://cloud.google.com/sdk]) - Needed to run ```gcloud``` commands in a terminal window.
* [Grafana Cloud](https://grafana.com/auth/sign-up/create-user) - Needed to send and visualize metrics and logs data.
* [Python](https://www.python.org/downloads/) - The walk-thru is packaged as a simple python CLI that can be re-purposed 
with ANY configuration management tool.

## Quickstart Guide
### Step 1
Git clone grafana-labs-sandbox. Each folder in the sandbox is dedicated to a specific 
use case. All files required for this walk-thru reside in the ```log-demo``` folder.

```
git clone https://github.com/cfossguy/grafana-labs-sandbox
cd ./log-demo
```

### Step 2
Make sure that you have a file named ```.env``` that is *NOT* checked into source control. 
This file needs to contain the following properties. Some properties are secrets, hence
the disclaimer on checking into source control.

```
gcp_vm_name=YOUR_VM_NAME
gcp_project=YOUR_GCP_PROJECT
gcp_zone=YOUR_GCP_ZONE (we recommend: us-central1-a)
gcp_machine_type=YOUR_GCP_MACHINE TYPE (we recommend: e2-standard-2)
gcp_service_account=YOUR_GCP_SERVICE_ACCOUNT

gcloud_username_metrics=YOUR_GRAFANA_CLOUD_METRICS_USERNAME
gcloud_username_logs=YOUR_GRAFANA_CLOUD_LOGS_USERNAME

gcloud_password_metrics=YOUR_GRAFANA_CLOUD_METRICS_PASSWORD
gcloud_password_logs=YOUR_GRAFANA_CLOUD_LOGS_PASSWORD

gcloud_remote_write_url_metrics=YOUR_GRAFANA_CLOUD_METRICS_REMOTE_WRITE_URL
gcloud_remote_write_url_logs=YOUR_GRAFANA_CLOUD_LOGS_REMOTE_WRITE_URL
```

### Step 3
Open a terminal window and run ```./demo``` to see the command line interface commands. 
Each command starts with a number to denote order. After a command runs, you will see
output for ```Next Run:```. Keep running commands until you see grafana agent output. 

CTRL+C will stop the grafana agent and halt metrics/logs collection. Let's let the agent
run in this terminal window.

### Step 4
Log into [Grafana](https://grafana.com/auth/sign-in/?plcmt=top-nav&cta=myaccount) and visualize your data. You can use 
[Integrations Management](https://jameswilliams1.grafana.net/a/grafana-easystart-app/integrations-management/integrations/linux-node) 
to install pre-built metrics dashboards for your Linux VM. You can skip grafana agent installation because the agent is already installed.

* You can use ```Explore``` for the label ```{app=tomcat_app}``` on the Prometheus datasource.
* You can use ```Explore``` for the labels ```{server=tomcat_server}``` and ```{app=tomcat_app}```on the Logs datasource.
* OPTIONAL - You can edit ```grafana-agent-template.yaml``` and re-run **Step 3**. This is handy for testing different 
grafana agent configuration settings. You can change the agent labels, log destinations, scrape intervals and more.

### Step 5
Free up the google cloud infrastructure you created by running ```./demo 6.teardown```. This will delete ALL installed
software and your VM. Grafana Cloud will still have the metrics and logs data that was sent prior to teardown.

### Troubleshooting
**Infrastructure as code** sometimes zigs when it should zag. If you need to debug an issue, run: ```./demo ssh```. 
This will ssh into the VM so that you can inspect the file system and running processes. While in SSH mode you can:
1. ```ps -ef | grep tomcat``` - Will let you know if tomcat is running on the VM
2. ```ps -ef | grep tomcat``` - Will let you know if the grafana agent is running on the VM
3. ```kill -9 PID``` - Handy if you want to retry a demo command without tearing down the whole VM
4. Run any ```os.system``` command in ```demo.py``` manually. For example, line 117 uses this command: ```./agent-linux-amd64 -config.file ./grafana-agent.yaml```
to start the grafana agent process. 
