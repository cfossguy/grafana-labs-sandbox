local gem = import 'github.com/grafana/jsonnet-libs/enterprise-metrics/main.libsonnet';

gem {
  _config+:: {
    commonArgs+:: {
      'cluster-name': 'ge',
      'admin.client.backend-type': 's3',
      'admin.client.s3.access-key-id': 'minio',
      'admin.client.s3.bucket-name': 'grafana-metrics-admin',
      'admin.client.s3.endpoint': 'minio:9000',
      'admin.client.s3.insecure': true,
      'admin.client.s3.secret-access-key': 'minio123',
      'blocks-storage.backend': 's3',
      'blocks-storage.s3.access-key-id': 'minio',
      'blocks-storage.s3.bucket-name': 'grafana-metrics-tsdb',
      'blocks-storage.s3.endpoint': 'minio:9000',
      'blocks-storage.s3.insecure': true,
      'blocks-storage.s3.secret-access-key': 'minio123',
    },
  },
  // Run without an alertmanager or ruler.
  alertmanager:: null,
  ruler:: null,
  // Make tokengen manifests available on a first run.
  tokengen+::: {}
}
