# Cyfox k3s Deployment

This directory contains Kubernetes manifests for deploying Cyfox to your k3s cluster.

## Prerequisites

- k3s cluster running on Raspberry Pi Zero 2W
- Argon40 Pod Display connected
- Docker image built and available in your cluster

## Deployment Steps

1. **Build and push Docker image** (adjust registry as needed):
   ```bash
   docker build -t cyfox:latest .
   # If using a registry:
   # docker tag cyfox:latest your-registry/cyfox:latest
   # docker push your-registry/cyfox:latest
   ```

2. **Apply manifests**:
   ```bash
   kubectl apply -f namespace.yaml
   kubectl apply -f configmap.yaml
   kubectl apply -f deployment.yaml
   ```

3. **Check deployment**:
   ```bash
   kubectl get pods -n cyfoxlab
   kubectl logs -n cyfoxlab -l app=cyfox
   ```

## Important Notes

- The deployment uses `hostNetwork: true` and `hostPID: true` for GPIO and display access
- The container runs with `privileged: true` for hardware access
- Adjust `nodeSelector` in deployment.yaml to match your node labels
- The configmap can be updated and pods will need to be restarted to pick up changes

## Troubleshooting

If the display doesn't work:
- Ensure the Argon40 Pod drivers are installed on the host
- Check that the display is properly connected
- Verify GPIO permissions

If buttons don't work:
- Check GPIO pin mappings in configmap
- Verify RPi.GPIO library is installed
- Check container logs for GPIO errors

