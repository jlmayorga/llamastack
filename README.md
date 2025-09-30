# Summit Connect AI Demo


1. Create new environment using this [catalog item](https://catalog.demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.ocp4-demo-rhods-nvidia-gpu-aws.prod&utm_source=webapp&utm_medium=share-link)
2. Upgrade OpenShift AI Operator to 2.23.0 - Fast
3. Update the GPU MachineSet resource to use `g6e.2xlarge` instance type
4. Ensure that the DataScienceCluster resource has `llamastackoperator` management state set to true
5. Apply all the resources

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
- https://github.com/opendatahub-io/llama-stack-k8s-operator/blob/odh/release/operator.yaml
- https://github.com/redhat-ai-services/modelcar-catalog
- https://docs.nvidia.com/datacenter/cloud-native/openshift/latest/steps-overview.html






