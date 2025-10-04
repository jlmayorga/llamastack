# LlamaStack Playground Helm Chart

This chart deploys the Streamlit-based LlamaStack Playground UI on OpenShift. It converts the original kustomize manifests in `llamastack/llamastack-playground/` into a parameterized Helm chart.

## Prerequisites
- OpenShift cluster with default router (for Route) or configure your own ingress.
- Helm 3.x

## Install
```bash
# Create/choose a namespace
oc new-project summit-connect-2025 || true

# Install with defaults (mirrors original manifests)
helm install my-playground ./charts/llamastack-playground -n summit-connect-2025
```

## Upgrade
```bash
helm upgrade my-playground ./charts/llamastack-playground -n summit-connect-2025
```

## Uninstall
```bash
helm uninstall my-playground -n summit-connect-2025
```

## Access
With route.enabled=true (default):
```bash
ROUTE=$(oc -n summit-connect-2025 get route my-playground-llamastack-playground -o jsonpath='{.spec.host}')
echo "https://${ROUTE}/"
```

## Values
The most relevant values (see values.yaml for full list):

- replicaCount: number of replicas (default 1)
- image:
  - repository: quay.io/rh-aiservices-bu/llama-stack-playground
  - tag: defaults to Chart.appVersion (0.2.11)
  - pullPolicy: IfNotPresent
- serviceAccount:
  - create: true to create a ServiceAccount
  - name: override name; defaults to chart fullname
  - annotations: {} map
- container:
  - name: llama-stack-playground
  - portName: http
  - port: 8501
  - env: STREAMLIT_* and LLAMA_STACK_ENDPOINT, DEFAULT_MODEL
  - envExtra: [] to append more env entries
- service:
  - type: ClusterIP
  - port: 80 (targets container portName)
- route:
  - enabled: true
  - host: optional fixed hostname
  - tls: termination (edge) and redirect policy
- resources: CPU/memory requests/limits
- livenessProbe / readinessProbe: probe tunables
- securityContext: pod and container security context
- labels/annotations: optional per-resource maps

## Example override
```yaml
replicaCount: 2
image:
  tag: "0.2.12"
container:
  env:
    LLAMA_STACK_ENDPOINT: "http://llamastack-service:8321"
    DEFAULT_MODEL: "llama32-3b"
route:
  host: playground.apps.example.com
```

## Notes
- Namespace is controlled by Helm's `--namespace` flag; templates do not hardcode namespace.
- The chart uses OpenShift Route for exposure; set `route.enabled=false` if you expose via another mechanism.
