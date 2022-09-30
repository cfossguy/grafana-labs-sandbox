variable "metrics_remote_write_url" {
  description = "Prometheus remote write URL - Grafana Cloud"
  type        = string
  sensitive   = true
}

variable "metrics_username" {
  description = "Prometheus remote write username - Grafana Cloud"
  type        = string
  sensitive   = true
}

variable "metrics_password" {
  description = "Prometheus remote write password - Grafana Cloud"
  type        = string
  sensitive   = true
}
