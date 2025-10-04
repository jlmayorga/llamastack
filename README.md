# Summit Connect AI Demo

1. Create new environment using this [catalog item](https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.ocp4-demo-rhods-nvidia-gpu-aws.prod&utm_source=webapp&utm_medium=share-link)
2. Upgrade OpenShift AI Operator to 2.23.0 - Fast
3. **Optional** Update the GPU MachineSet resource to use `g6e.2xlarge` instance type
4. Ensure that the DataScienceCluster resource has `llamastackoperator` management state set to true
5. oc patch dsc default-dsc --type='merge' --patch-file datasciencecluster/datasciencecluster-patch.yaml
6. create project summit-connect-2025
7. Apply all the resources
   - `oc apply -k trustyai_fms`
   - `oc apply -k llama-3`
   - 
> [! IMPORTANT]
> Important: Scale down the GPU MachineSet to 0 every day to avoid wasteful charges
> ```
> oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) --replicas=0 -n openshift-machine-api
> ```

## TODO
- Implement guardrails with [TrustyAI FMS](https://trustyai.org/docs/main/trustyai-fms-lls-tutorial)

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






