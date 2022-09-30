resource "kubernetes_manifest" "configmap_spring_apps_grafana_agent" {
  manifest = {
    "apiVersion" = "v1"
    "data" = {
      "agent.yaml" = <<-EOT
      metrics:
        wal_directory: /tmp/grafana-agent-spring-wal
        global:
          scrape_interval: 60s
          external_labels:
            app: spring-node
        configs:
        - name: spring-apps
          remote_write:
          - url: ${var.metrics_remote_write_url}
            basic_auth:
              username: ${var.metrics_username}
              password: ${var.metrics_password}
          scrape_configs:
          - job_name: spring-apps/spring-boot
            metrics_path: /actuator/prometheus
            kubernetes_sd_configs:
              - role: endpoints
      EOT
    }
    "kind" = "ConfigMap"
    "metadata" = {
      "name" = "grafana-agent-spring"
      "namespace" = "spring-apps"
    }
  }
}

resource "kubernetes_manifest" "serviceaccount_spring_apps_grafana_agent" {
  manifest = {
    "apiVersion" = "v1"
    "kind" = "ServiceAccount"
    "metadata" = {
      "name" = "grafana-agent-spring"
      "namespace" = "spring-apps"
    }
  }
}

resource "kubernetes_manifest" "clusterrole_spring_apps_grafana_agent" {
  manifest = {
    "apiVersion" = "rbac.authorization.k8s.io/v1"
    "kind" = "ClusterRole"
    "metadata" = {
      "name" = "grafana-agent-spring"
    }
    "rules" = [
      {
        "apiGroups" = [
          "",
        ]
        "resources" = [
          "endpoints",
          "nodes",
          "nodes/proxy",
          "services",
          "endpoints",
          "pods",
          "events",
        ]
        "verbs" = [
          "get",
          "list",
          "watch",
        ]
      },
      {
        "nonResourceURLs" = [
          "/metrics",
        ]
        "verbs" = [
          "get",
        ]
      },
    ]
  }
}

resource "kubernetes_manifest" "clusterrolebinding_spring_apps_grafana_agent" {
  manifest = {
    "apiVersion" = "rbac.authorization.k8s.io/v1"
    "kind" = "ClusterRoleBinding"
    "metadata" = {
      "name" = "grafana-agent-spring"
    }
    "roleRef" = {
      "apiGroup" = "rbac.authorization.k8s.io"
      "kind" = "ClusterRole"
      "name" = "grafana-agent-spring"
    }
    "subjects" = [
      {
        "kind" = "ServiceAccount"
        "name" = "grafana-agent-spring"
        "namespace" = "spring-apps"
      },
    ]
  }
}

resource "kubernetes_manifest" "service_spring_apps_grafana_agent" {
  manifest = {
    "apiVersion" = "v1"
    "kind" = "Service"
    "metadata" = {
      "labels" = {
        "name" = "grafana-agent-spring"
      }
      "name" = "grafana-agent-spring"
      "namespace" = "spring-apps"
    }
    "spec" = {
      "clusterIP" = "None"
      "ports" = [
        {
          "name" = "grafana-agent-spring-http-metrics"
          "port" = 80
          "targetPort" = 80
        },
      ]
      "selector" = {
        "name" = "grafana-agent-spring"
      }
    }
  }
}

resource "kubernetes_manifest" "statefulset_spring_apps_grafana_agent" {
  manifest = {
    "apiVersion" = "apps/v1"
    "kind" = "StatefulSet"
    "metadata" = {
      "name" = "grafana-agent-spring"
      "namespace" = "spring-apps"
    }
    "spec" = {
      "replicas" = 1
      "selector" = {
        "matchLabels" = {
          "name" = "grafana-agent-spring"
        }
      }
      "serviceName" = "grafana-agent-spring"
      "template" = {
        "metadata" = {
          "labels" = {
            "name" = "grafana-agent-spring"
          }
        }
        "spec" = {
          "containers" = [
            {
              "args" = [
                "-config.file=/etc/agent/agent.yaml",
                "-enable-features=integrations-next",
                "-server.http.address=0.0.0.0:80",
              ]
              "command" = [
                "/bin/agent",
              ]
              "env" = [
                {
                  "name" = "HOSTNAME"
                  "valueFrom" = {
                    "fieldRef" = {
                      "fieldPath" = "spec.nodeName"
                    }
                  }
                },
              ]
              "image" = "grafana/agent:v0.28.0"
              "imagePullPolicy" = "IfNotPresent"
              "name" = "grafana-agent-spring"
              "ports" = [
                {
                  "containerPort" = 80
                  "name" = "http-metrics"
                },
              ]
              "volumeMounts" = [
                {
                  "mountPath" = "/var/lib/agent"
                  "name" = "agent-wal"
                },
                {
                  "mountPath" = "/etc/agent"
                  "name" = "grafana-agent-spring"
                },
              ]
            },
          ]
          "serviceAccount" = "grafana-agent-spring"
          "volumes" = [
            {
              "configMap" = {
                "name" = "grafana-agent-spring"
              }
              "name" = "grafana-agent-spring"
            },
          ]
        }
      }
      "updateStrategy" = {
        "type" = "RollingUpdate"
      }
      "volumeClaimTemplates" = [
        {
          "apiVersion" = "v1"
          "kind" = "PersistentVolumeClaim"
          "metadata" = {
            "name" = "agent-wal"
            "namespace" = "spring-apps"
          }
          "spec" = {
            "accessModes" = [
              "ReadWriteOnce",
            ]
            "resources" = {
              "requests" = {
                "storage" = "1Gi"
              }
            }
          }
        },
      ]
    }
  }
}
