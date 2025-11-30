# k3s Deployment

Deploy Cyfox to your k3s cluster.

## Quick Deploy

```bash
kubectl apply -f k8s/
```

## Check Status

```bash
kubectl get pods -n cyfoxlab
kubectl logs -n cyfoxlab -l app=cyfox
```

## Notes

- Uses `hostNetwork: true` and `hostPID: true` for GPIO/display access
- Container runs with `privileged: true` for hardware access
- Adjust `nodeSelector` in `deployment.yaml` for your node labels

