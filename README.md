# Engineering Trustworthy AI - Summit Connect 2025 Demo

A demonstration of the **Decoupled Shield Pattern** for building trustworthy AI systems using OpenShift AI, LlamaStack, and TrustyAI.

## What This Demo Shows

This project demonstrates how to build AI agents with **architectural safety** rather than relying solely on model behavior. It showcases:

- **Decoupled Shield Pattern**: Safety logic separated from application code
- **Defense-in-Depth**: Input and output validation layers
- **Provider Flexibility**: Swap safety providers without code changes
- **Enterprise-Ready**: Audit trails, compliance, and centralized governance

### The Problem We Solve

AI agents are powerful but create trust gaps:
- How do we prevent PII leaks?
- How do we stop prompt injections?
- How do we ensure content policy compliance at scale?

Traditional approaches embed safety in code, creating vendor lock-in and making verification difficult.

**Our approach**: Independent, reusable safety shields that protect multiple AI agents.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    OpenShift AI                         │
│                                                         │
│  ┌──────────────────┐         ┌──────────────────┐      │
│  │  LlamaStack      │────────▶│  Llama 3.2 1B    │      │
│  │  Distribution    │         │  (vLLM)          │      │
│  └────────┬─────────┘         └──────────────────┘      │
│           │                                             │
│           │ Shield API                                  │
│           ▼                                             │
│  ┌──────────────────┐         ┌──────────────────┐      │
│  │  TrustyAI FMS    │         │  LlamaStack      │      │
│  │  Orchestrator    │         │  Playground UI   │      │
│  │  - Email         │         └──────────────────┘      │
│  │  - SSN           │                                   │
│  │  - Credit Card   │                                   │
│  └──────────────────┘                                   │
└─────────────────────────────────────────────────────────┘
```

### Components

1. **LlamaStack Distribution** (`llamastack-trustyai-fms`)
   - Manages model inference and shield orchestration
   - Integrates with TrustyAI for safety checks
   - Provides unified API for agents

2. **Model Serving** (KServe + vLLM)
   - Llama 3.2 1B (instruction-tuned)
   - Granite Embedding 125M
   - GPU-accelerated inference

3. **TrustyAI Guardrails Orchestrator**
   - Regex-based PII detection (email, SSN, credit card)
   - Fast, deterministic validation
   - Input and output shield support

4. **LlamaStack Playground**
   - Web UI for testing agents
   - Visual shield configuration
   - Real-time validation feedback

## Prerequisites

### OpenShift Cluster
- OpenShift 4.18+
- GPU node(s) with NVIDIA drivers
  - Recommended: AWS `g6e.2xlarge` or similar
  - At least 1 GPU per model
- Node Feature Discovery (NFD) operator installed
- NVIDIA GPU operator installed

### OpenShift AI
- Version: 2.23.0
- Components enabled:
  - Model Serving (KServe)
  - LlamaStack Operator
  - TrustyAI

### Other
- `oc` CLI tool
- Cluster admin access
- ~100GB storage for models

## Quick Start

### 1. Provision Environment

Use the Red Hat Demo Platform catalog item:
- [OpenShift with RHOAI + NVIDIA GPU](https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.ocp4-demo-rhods-nvidia-gpu-aws.prod)

Or configure your own cluster with GPU support.

### 2. Upgrade OpenShift AI

```bash
# Ensure you're running OpenShift AI 2.23.0
# Via OperatorHub: OpenShift AI Operator → Fast channel → 2.23.0
```

### 3. Enable LlamaStack Operator

```bash
# Patch the DataScienceCluster to enable LlamaStack
oc patch datasciencecluster default-dsc --type='merge' -p '{"spec":{"components":{"llamastack":{"managementState":"Managed"}}}}'
```

### 4. Create Project

```bash
oc apply -f project.yml
```

### 5. Deploy Everything

```bash
# Deploy all components using Kustomize
oc apply -k demo/

# Monitor deployment
oc get pods -n summit-connect-2025 -w
```

This will deploy:
- Model serving runtime (vLLM)
- Llama 3.2 1B inference service
- TrustyAI Guardrails Orchestrator
- LlamaStack distribution with TrustyAI integration
- LlamaStack Playground UI

### 6. Wait for Components

```bash
# Check model serving
oc wait --for=condition=Ready pod -l serving.kserve.io/inferenceservice=llama32-1b -n summit-connect-2025 --timeout=10m

# Check LlamaStack
oc wait --for=condition=Ready pod -l app.kubernetes.io/name=llamastack-trustyai-fms -n summit-connect-2025 --timeout=5m

# Check Playground
oc wait --for=condition=Ready pod -l app.kubernetes.io/name=llamastack-playground-trustyai -n summit-connect-2025 --timeout=3m
```

### 7. Access the Demo

Get the playground URL:
```bash
oc get route llamastack-playground-trustyai -n summit-connect-2025 -o jsonpath='{.spec.host}'
```

Get the LlamaStack API URL:
```bash
oc get route llamastack-trustyai-fms -n summit-connect-2025 -o jsonpath='{.spec.host}'
```

## Demo Notebooks

Two Jupyter notebooks are included in the `notebooks/` directory:

### 1. `safety-demo.ipynb` - Core Shield Pattern Demo
- Demonstrates input and output shields
- Shows PII detection in action
- Compares protected vs unprotected agents
- **Best for**: Live coding demos

### 2. `llamastack-client-2.ipynb` - Multi-Provider Comparison
- Compares TrustyAI (regex) vs Llama Guard (ML-based)
- Shows complementary strengths
- Demonstrates provider flexibility
- **Best for**: Architecture discussions

### Running Notebooks

1. Upload notebooks to your OpenShift AI workbench
2. Update the `LLAMASTACK_URL` to your deployed endpoint
3. Run cells sequentially

## Project Structure

```
.
├── demo/
│   ├── kustomization.yml           # Main kustomize entry point
│   ├── models/llama-3/             # Model serving configs
│   │   ├── servingruntime.yml      # vLLM runtime
│   │   ├── inferenceservice.yml    # Llama 3.2 1B service
│   │   └── connection-secret.yml   # Model registry credentials
│   ├── llamastack/
│   │   ├── llamastack-trustyai-fms/  # LlamaStack distribution
│   │   └── playground/               # Playground UI deployment
│   └── trustyai/trustyai_fms/      # TrustyAI guardrails config
├── notebooks/
│   ├── safety-demo.ipynb           # Main demo notebook
│   └── llamastack-client-2.ipynb   # Multi-provider demo
└── README.md
```

## Key Configuration Files

### LlamaStack Distribution
- File: `demo/llamastack/llamastack-trustyai-fms/llamastackdistribution.yml`
- Connects to vLLM inference and TrustyAI orchestrator
- Exposes unified API on port 8321

### TrustyAI Guardrails
- File: `demo/trustyai/trustyai_fms/guardrailsorchestrator.yml`
- Configures built-in PII detectors
- Regex patterns for email, SSN, credit card

### Shield Registration
Shields are registered programmatically via the LlamaStack API:

```python
client.shields.register(
    shield_id="pii_shield",
    provider_id="trustyai_fms",
    params={
        "type": "content",
        "confidence_threshold": 0.8,
        "detectors": {
            "regex": {
                "detector_params": {
                    "regex": ["email", "ssn", "credit-card"]
                }
            }
        }
    }
)
```

## Cost Management

**IMPORTANT**: GPU instances are expensive. Scale down when not in use:

```bash
# Scale down GPU MachineSets
oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) --replicas=0 -n openshift-machine-api

# Scale up when needed
oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) --replicas=1 -n openshift-machine-api
```

## Troubleshooting

### Model Pod Won't Start
```bash
# Check GPU availability
oc describe node $(oc get nodes -l node-role.kubernetes.io/worker -o name | head -1)

# Check model pod logs
oc logs -n summit-connect-2025 -l serving.kserve.io/inferenceservice=llama32-1b --tail=50
```

### LlamaStack Can't Connect to TrustyAI
```bash
# Verify TrustyAI is running
oc get pods -n summit-connect-2025 | grep guardrails

# Check LlamaStack environment variables
oc get deployment llamastack-trustyai-fms -n summit-connect-2025 -o yaml | grep -A 10 env:

# Test connectivity from LlamaStack pod
oc exec -n summit-connect-2025 deployment/llamastack-trustyai-fms -- curl http://guardrails-orchestrator-service:8033/health
```

### Shield Registration Fails
```bash
# Check TrustyAI logs
oc logs -n summit-connect-2025 -l app=guardrails-orchestrator --tail=100

# Verify shield configuration
oc get configmap fms-orchestr8-config-nlp -n summit-connect-2025 -o yaml
```

### Playground Won't Load
```bash
# Check playground logs
oc logs -n summit-connect-2025 -l app.kubernetes.io/name=llamastack-playground-trustyai

# Verify route
oc get route llamastack-playground-trustyai -n summit-connect-2025
```

## Resources

### Documentation
- [OpenShift AI 2.23 Docs](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.23)
- [LlamaStack Documentation](https://llama-stack.readthedocs.io/)
- [TrustyAI Documentation](https://trustyai.org/docs/)
- [vLLM Documentation](https://docs.vllm.ai/)

### Related Projects
- [TrustyAI FMS Provider](https://github.com/trustyai-explainability/llama-stack-provider-trustyai-fms)
- [LlamaStack K8s Operator](https://github.com/opendatahub-io/llama-stack-k8s-operator)
- [ModelCar Catalog](https://github.com/redhat-ai-services/modelcar-catalog)
- [Red Hat AI Quickstarts](https://github.com/rh-ai-quickstart)

### Instance Types
- [AWS G6e Instances](https://aws.amazon.com/ec2/instance-types/g6e/) - Recommended for this demo


Resources

- [AWS Instance types](https://aws.amazon.com/ec2/instance-types/g6e/)
- https://github.com/rh-aiservices-bu/lls-operator-demo
- https://github.com/rh-aiservices-bu/llama-stack-tutorial
- https://github.com/redhat-ai-services/llama-stack-playground
- https://github.com/redhat-et/agent-frameworks
- https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2.23/html/working_with_rag/deploying-a-rag-stack-in-a-data-science-project_rag
- https://llama-stack-k8s-operator.pages.dev/distributions/vllm/
- https://github.com/burrsutter/llama-stack-tutorial
- https://github.com/opendatahub-io/llama-stack-distribution/blob/rhoai-v2.22/redhat-distribution/run.yaml
- https://github.com/alpha-hack-program/rag-base/blob/b805401667b1b349f4be92acb67a531c78f0adf5/gitops/rag-lsd/templates/run.yaml
- https://github.com/opendatahub-io/llama-stack-k8s-operator/blob/odh/release/operator.yaml
- https://github.com/redhat-ai-services/modelcar-catalog
- https://docs.nvidia.com/datacenter/cloud-native/openshift/latest/steps-overview.html
- https://github.com/opendatahub-io/llama-stack-distribution/tree/main/distribution
- https://trustyai.org/docs/main/trustyai-fms-lls-tutorial
- https://github.com/ruivieira/llama-stack-provider-trustyai-fms
- https://github.com/red-hat-data-services/llama-stack-distribution
- https://github.com/trustyai-explainability/trustyai-llm-demo/tree/main/guardrails-quickstart-demo
- https://github.com/alvarolop/mcp-playground/blob/a1b6e6da82b03be2c2a91b78e37a394ee655fd42/llama-stack-chart/templates/secret.yaml
- https://github.com/opendatahub-io/llama-stack-demos/blob/main/demos/rag_agentic/notebooks/Level0_getting_started_with_Llama_Stack.ipynb
- https://github.com/trustyai-explainability/llama-stack-provider-trustyai-fms/blob/main/runtime_configurations/detector_api.yaml
- https://github.com/rh-ai-quickstart/lls-observability
- https://github.com/rh-ai-quickstart/guardrailing-llms/blob/main/helm/templates/guardrails-orchestrator.yaml
- https://github.com/rh-ai-quickstart/ai-architecture-charts






