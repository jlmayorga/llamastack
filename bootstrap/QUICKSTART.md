# Bootstrap Quick Start

## Prerequisites Check

```bash
# Run verification script first
./verify.sh
```

## Installation

```bash
# 1. Install Ansible dependencies
make install-deps

# 2. Run bootstrap (this will take 5-10 minutes)
make bootstrap

# 3. Verify completion
make check-cluster
```

## What Gets Configured

- ✓ OpenShift AI upgraded to 2.23.0
- ✓ LlamaStack operator enabled
- ✓ GPU nodes scaled up (1 replica)
- ✓ Demo namespace created (`summit-connect-2025`)
- ✓ Prerequisites validated

## Next Steps

After successful bootstrap:

```bash
# Deploy the demo
cd ..
oc apply -k demo/

# Watch deployment
oc get pods -n summit-connect-2025 -w

# Wait for models (takes ~5-10 minutes)
oc wait --for=condition=Ready pod \
  -l serving.kserve.io/inferenceservice=llama32-1b \
  -n summit-connect-2025 --timeout=10m

# Get playground URL
echo "https://$(oc get route llamastack-playground-trustyai -n summit-connect-2025 -o jsonpath='{.spec.host}')"
```

## Cost Saving

When done with demo:

```bash
# Scale down GPU nodes (saves $$)
make scale-down-gpu

# Scale back up when needed
make scale-up-gpu
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Ansible not found | `pip install ansible` |
| OpenShift AI not installed | Install via OperatorHub first |
| GPU nodes not found | Install NFD and NVIDIA GPU operators |
| Permission denied | Ensure you're logged in as cluster-admin |

## Custom Configuration

Edit variables in `bootstrap.yml`:

```yaml
vars:
  target_openshift_ai_version: "2.23.0"
  target_channel: "fast"
  gpu_machineset_replicas: 1
  demo_namespace: "summit-connect-2025"
```

Or pass via command line:

```bash
ansible-playbook bootstrap.yml -e "gpu_machineset_replicas=2"
```

## Files

- `bootstrap.yml` - Main playbook
- `verify.sh` - Pre-flight checks
- `Makefile` - Convenience commands
- `README.md` - Full documentation
