# Dual GPU Deployment

This overlay deploys the demo with **both Llama 3.2 1B and TinyLlama** for model comparison and testing.

## What's Deployed

✅ TinyLlama 1B model (tinyllama-1b) - GPU 1
✅ Llama 3.2 1B model (llama32-1b) - GPU 2
✅ LlamaStack distribution (configured for tinyllama-1b by default)
✅ TrustyAI guardrails orchestrator
✅ Playground UI

## Prerequisites

- **2 GPU nodes** available
- ~40GB GPU memory total (20GB per model)
- OpenShift AI 2.23.0+
- TrustyAI and LlamaStack operators enabled

## Scale Up GPU Nodes

Before deploying, ensure you have 2 GPU nodes:

```bash
# Check current GPU nodes
oc get nodes -l nvidia.com/gpu.present=true

# Scale up to 2 replicas
oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) \
  --replicas=2 -n openshift-machine-api

# Wait for nodes to be ready (takes ~5-10 minutes)
oc wait --for=condition=Ready node -l nvidia.com/gpu.present=true \
  --timeout=10m
```

## Deployment

```bash
# From repository root
oc apply -k demo/overlays/dual-gpu/
```

## When to Use

- **Model comparison**: Test different model sizes/quality
- **Development**: Need multiple models for testing
- **Demonstrations**: Show model switching capabilities
- **High availability**: Fallback models available

## Switching Between Models

LlamaStack uses tinyllama-1b by default. To switch to Llama 3.2:

```bash
oc patch llamastackdistribution llamastack-trustyai-fms \
  -n summit-connect-2025 --type='json' -p='[
  {"op": "replace", "path": "/spec/server/containerSpec/env/0/value",
   "value": "http://llama32-1b-predictor:8080/v1"},
  {"op": "replace", "path": "/spec/server/containerSpec/env/1/value",
   "value": "llama32-1b"}
]'
```

## Cost Management

⚠️ **Important**: Dual GPU deployment is **expensive** (~$1.50-2.00/hour on AWS)

Scale down when not in use:

```bash
# Scale down GPU nodes
oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) \
  --replicas=0 -n openshift-machine-api

# Or scale down to 1 GPU
oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) \
  --replicas=1 -n openshift-machine-api
```
