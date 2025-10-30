# Single GPU Deployment

This overlay deploys the demo with **only TinyLlama 1B** to avoid GPU exhaustion on clusters with a single GPU node.

## What's Deployed

✅ TinyLlama 1B model (tinyllama-1b)
✅ LlamaStack distribution (configured for tinyllama-1b)
✅ TrustyAI guardrails orchestrator
✅ Playground UI
❌ Llama 3.2 (excluded to save GPU resources)

## Prerequisites

- 1 GPU node available
- ~20GB GPU memory
- OpenShift AI 2.23.0+
- TrustyAI and LlamaStack operators enabled

## Deployment

```bash
# From repository root
oc apply -k demo/overlays/single-gpu/
```

## When to Use

- **Cost optimization**: Single GPU node is cheaper
- **Quick demos**: Faster to provision one model
- **Production**: Most use cases only need one model
- **Limited resources**: Only 1 GPU node available

## Switching Models

To use Llama 3.2 instead of TinyLlama:

1. Edit the LlamaStack distribution:
   ```bash
   oc patch llamastackdistribution llamastack-trustyai-fms \
     -n summit-connect-2025 --type='json' -p='[
     {"op": "replace", "path": "/spec/server/containerSpec/env/0/value",
      "value": "http://llama32-1b-predictor.summit-connect-2025.svc.cluster.local:8080/v1"},
     {"op": "replace", "path": "/spec/server/containerSpec/env/1/value",
      "value": "llama32-1b"}
   ]'
   ```

2. Deploy Llama 3.2 and scale down TinyLlama:
   ```bash
   oc apply -k demo/models/llama-3/
   oc scale deployment tinyllama-1b-predictor -n summit-connect-2025 --replicas=0
   ```

## Cost Saving

When done with demo:

```bash
# Scale down GPU nodes
oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) \
  --replicas=0 -n openshift-machine-api
```
