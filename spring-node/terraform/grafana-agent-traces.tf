resource "kubernetes_manifest" "serviceaccount_spring_apps_grafana_agent_traces" {
  manifest = {
    "apiVersion" = "v1"
    "kind" = "ServiceAccount"
    "metadata" = {
      "name" = "grafana-agent-spring-traces"
      "namespace" = "spring-apps"
    }
  }
}

resource "kubernetes_manifest" "clusterrole_spring_apps_grafana_agent_traces" {
  manifest = {
    "apiVersion" = "rbac.authorization.k8s.io/v1"
    "kind" = "ClusterRole"
    "metadata" = {
      "name" = "grafana-agent-spring-traces"
    }
    "rules" = [
      {
        "apiGroups" = [
          "",
        ]
        "resources" = [
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

resource "kubernetes_manifest" "clusterrolebinding_spring_apps_grafana_agent_traces" {
  manifest = {
    "apiVersion" = "rbac.authorization.k8s.io/v1"
    "kind" = "ClusterRoleBinding"
    "metadata" = {
      "name" = "grafana-agent-spring-traces"
    }
    "roleRef" = {
      "apiGroup" = "rbac.authorization.k8s.io"
      "kind" = "ClusterRole"
      "name" = "grafana-agent-spring-traces"
    }
    "subjects" = [
      {
        "kind" = "ServiceAccount"
        "name" = "grafana-agent-spring-traces"
        "namespace" = "spring-apps"
      },
    ]
  }
}

resource "kubernetes_manifest" "service_spring_apps_grafana_agent_traces" {
  manifest = {
    "apiVersion" = "v1"
    "kind" = "Service"
    "metadata" = {
      "labels" = {
        "name" = "grafana-agent-spring-traces"
      }
      "name" = "grafana-agent-spring-traces"
      "namespace" = "spring-apps"
    }
    "spec" = {
      "ports" = [
        {
          "name" = "grafana-agent-spring-traces-http-metrics"
          "port" = 80
          "targetPort" = 80
        },
        {
          "name" = "grafana-agent-spring-traces-thrift-compact"
          "port" = 6831
          "protocol" = "UDP"
          "targetPort" = 6831
        },
        {
          "name" = "grafana-agent-spring-traces-thrift-binary"
          "port" = 6832
          "protocol" = "UDP"
          "targetPort" = 6832
        },
        {
          "name" = "grafana-agent-spring-traces-thrift-http"
          "port" = 14268
          "protocol" = "TCP"
          "targetPort" = 14268
        },
        {
          "name" = "grafana-agent-spring-traces-thrift-grpc"
          "port" = 14250
          "protocol" = "TCP"
          "targetPort" = 14250
        },
        {
          "name" = "grafana-agent-spring-traces-zipkin"
          "port" = 9411
          "protocol" = "TCP"
          "targetPort" = 9411
        },
        {
          "name" = "grafana-agent-spring-traces-otlp"
          "port" = 4317
          "protocol" = "TCP"
          "targetPort" = 4317
        },
        {
          "name" = "grafana-agent-spring-traces-opencensus"
          "port" = 55678
          "protocol" = "TCP"
          "targetPort" = 55678
        },
      ]
      "selector" = {
        "name" = "grafana-agent-spring-traces"
      }
    }
  }
}

resource "kubernetes_manifest" "deployment_spring_apps_grafana_agent_traces" {
  manifest = {
    "apiVersion" = "apps/v1"
    "kind" = "Deployment"
    "metadata" = {
      "name" = "grafana-agent-spring-traces"
      "namespace" = "spring-apps"
    }
    "spec" = {
      "minReadySeconds" = 10
      "replicas" = 1
      "revisionHistoryLimit" = 10
      "selector" = {
        "matchLabels" = {
          "name" = "grafana-agent-spring-traces"
        }
      }
      "template" = {
        "metadata" = {
          "labels" = {
            "name" = "grafana-agent-spring-traces"
          }
        }
        "spec" = {
          "containers" = [
            {
              "args" = [
                "-config.file=/etc/agent/agent.yaml",
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
              "image" = "grafana/agent:v0.26.1"
              "imagePullPolicy" = "IfNotPresent"
              "name" = "grafana-agent-spring-traces"
              "ports" = [
                {
                  "containerPort" = 80
                  "name" = "http-metrics"
                },
                {
                  "containerPort" = 6831
                  "name" = "thrift-compact"
                  "protocol" = "UDP"
                },
                {
                  "containerPort" = 6832
                  "name" = "thrift-binary"
                  "protocol" = "UDP"
                },
                {
                  "containerPort" = 14268
                  "name" = "thrift-http"
                  "protocol" = "TCP"
                },
                {
                  "containerPort" = 14250
                  "name" = "thrift-grpc"
                  "protocol" = "TCP"
                },
                {
                  "containerPort" = 9411
                  "name" = "zipkin"
                  "protocol" = "TCP"
                },
                {
                  "containerPort" = 4317
                  "name" = "otlp"
                  "protocol" = "TCP"
                },
                {
                  "containerPort" = 55678
                  "name" = "opencensus"
                  "protocol" = "TCP"
                },
              ]
              "volumeMounts" = [
                {
                  "mountPath" = "/etc/agent"
                  "name" = "grafana-agent-spring-traces"
                },
              ]
            },
          ]
          "serviceAccount" = "grafana-agent-spring-traces"
          "volumes" = [
            {
              "configMap" = {
                "name" = "grafana-agent-spring-traces"
              }
              "name" = "grafana-agent-spring-traces"
            },
          ]
        }
      }
    }
  }
}


resource "kubernetes_manifest" "configmap_spring_apps_grafana_agent_traces" {
  manifest = {
    "apiVersion" = "v1"
    "data" = {
      "agent.yaml" = <<-EOT
      server:
          log_level: debug
      tempo:
          configs:
            - batch:
                  send_batch_size: 1000
                  timeout: 5s
              name: default
              receivers:
                  zipkin:
              remote_write:
                - basic_auth:
                      password: ${var.traces_password}
                      username: ${var.traces_username}
                  endpoint: ${var.traces_url}
                  retry_on_failure:
                      enabled: false
              scrape_configs:
                - bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
                  job_name: kubernetes-pods
                  kubernetes_sd_configs:
                    - role: pod
                  relabel_configs:
                    - action: replace
                      source_labels:
                        - __meta_kubernetes_namespace
                      target_label: namespace
                    - action: replace
                      source_labels:
                        - __meta_kubernetes_pod_name
                      target_label: pod
                    - action: replace
                      source_labels:
                        - __meta_kubernetes_pod_container_name
                      target_label: container
                  tls_config:
                      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
                      insecure_skip_verify: false
      
      EOT
      "strategies.json" = "{\"default_strategy\": {\"param\": 0.001, \"type\": \"probabilistic\"}}"
    }
    "kind" = "ConfigMap"
    "metadata" = {
      "name" = "grafana-agent-spring-traces"
      "namespace" = "spring-apps"
    }
  }
}
