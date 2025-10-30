# Bootstrap OpenShift Cluster for LlamaStack Demo

This directory contains Ansible playbooks to prepare your OpenShift cluster for the LlamaStack TrustyAI demo.

## Prerequisites

- OpenShift cluster (4.18+) with cluster-admin access
- `oc` CLI installed and logged in
- Ansible 2.9+ installed
- Python 3.8+
- OpenShift AI operator already installed (any version)

## Quick Start

```bash
# Install Ansible dependencies
make install-deps

# Run the bootstrap playbook
make bootstrap

# Or run with verbose output
make bootstrap-verbose
```

## What the Bootstrap Does

The playbook automatically:

1. **Verifies cluster access** - Checks `oc` CLI and authentication
2. **Upgrades OpenShift AI** - Patches subscription to version 2.23.0 if needed
3. **Enables LlamaStack operator** - Configures DataScienceCluster
4. **Checks GPU operators** - Verifies NFD and NVIDIA GPU operator installation
5. **Scales GPU nodes** - Ensures GPU machinesets have at least 1 replica
6. **Creates demo namespace** - Sets up `summit-connect-2025` namespace
7. **Validates prerequisites** - Checks storage and other requirements

## Manual Execution

If you prefer to run Ansible directly:

```bash
# Install required Ansible collections
ansible-galaxy collection install -r requirements.yml

# Run the playbook
ansible-playbook bootstrap.yml

# Run with extra verbosity
ansible-playbook bootstrap.yml -vv

# Run with custom variables
ansible-playbook bootstrap.yml -e "gpu_machineset_replicas=2"
```

## Configuration Variables

You can customize the bootstrap by editing [bootstrap.yml](bootstrap.yml) or passing variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `target_openshift_ai_version` | `2.23.0` | Target OpenShift AI version |
| `target_channel` | `fast` | Operator subscription channel |
| `demo_namespace` | `summit-connect-2025` | Demo namespace name |
| `gpu_machineset_replicas` | `1` | Number of GPU node replicas |
| `operator_timeout` | `600` | Operator upgrade timeout (seconds) |

Example with custom variables:

```bash
ansible-playbook bootstrap.yml \
  -e "target_channel=stable" \
  -e "gpu_machineset_replicas=2"
```

## Post-Bootstrap Steps

After successful bootstrap:

1. **Deploy the demo**:
   ```bash
   cd ..
   oc apply -k demo/
   ```

2. **Monitor deployment**:
   ```bash
   oc get pods -n summit-connect-2025 -w
   ```

3. **Wait for models to be ready**:
   ```bash
   oc wait --for=condition=Ready pod \
     -l serving.kserve.io/inferenceservice=llama32-1b \
     -n summit-connect-2025 --timeout=10m
   ```

4. **Get playground URL**:
   ```bash
   oc get route llamastack-playground-trustyai \
     -n summit-connect-2025 \
     -o jsonpath='{.spec.host}'
   ```

## Troubleshooting

### OpenShift AI Upgrade Fails

Check available channels:
```bash
oc get packagemanifest rhods-operator \
  -n openshift-marketplace \
  -o jsonpath='{.status.channels[*].name}'
```

Manually patch subscription:
```bash
oc patch subscription rhods-operator \
  -n redhat-ods-operator \
  --type='merge' \
  -p '{"spec":{"channel":"fast"}}'
```

### GPU Nodes Not Available

Check if GPU operators are installed:
```bash
# Node Feature Discovery
oc get subscription nfd -n openshift-nfd

# NVIDIA GPU Operator
oc get subscription -n nvidia-gpu-operator
```

Install via OperatorHub if missing.

### Namespace Already Exists

The playbook will reuse the existing namespace. If you need a fresh start:
```bash
oc delete namespace summit-connect-2025
```

Then re-run the bootstrap.

### LlamaStack Operator Not Enabled

Manually enable:
```bash
oc patch datasciencecluster default-dsc --type='merge' \
  -p '{"spec":{"components":{"llamastack":{"managementState":"Managed"}}}}'
```

## Cost Management

GPU instances are expensive. After demoing, scale down GPU nodes:

```bash
# Scale down
make scale-down-gpu

# Scale back up
make scale-up-gpu

# Or manually
oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) \
  --replicas=0 -n openshift-machine-api
```

## Files

- **[bootstrap.yml](bootstrap.yml)** - Main Ansible playbook
- **[requirements.yml](requirements.yml)** - Ansible collection dependencies
- **[inventory.yml](inventory.yml)** - Ansible inventory (localhost)
- **[ansible.cfg](ansible.cfg)** - Ansible configuration
- **[Makefile](Makefile)** - Convenience targets for common tasks

## Support

For issues specific to this bootstrap:
1. Check the playbook output for error messages
2. Review the troubleshooting section above
3. Examine OpenShift logs: `oc logs -n redhat-ods-operator <pod-name>`

For demo-specific issues, see the main [README.md](../README.md).
