#/bin/sh

# Install kubectl directpv plugin
kubectl krew install directpv

# Use the plugin to install directpv in your kubernetes cluster
kubectl directpv install

# give directpv crd time to install
sleep 30

# Ensure directpv has successfully started
kubectl directpv info

# List available drives in your cluster
kubectl directpv drives ls

# Format local drives in your cluster
kubectl directpv drives format --drives /dev/sdb --nodes se-jwilliams-rancher-node1-vm
kubectl directpv drives format --drives /dev/sdb --nodes se-jwilliams-rancher-node2-vm
kubectl directpv drives format --drives /dev/sdb --nodes se-jwilliams-rancher-node3-vm

# Ensure directpv has successfully started
kubectl directpv info

# set directpv as the default storage class
kubectl patch storageclass direct-csi-min-io -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

kubectl get storageclass