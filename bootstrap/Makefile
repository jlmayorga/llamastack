.PHONY: help install-deps bootstrap bootstrap-verbose check-cluster scale-up-gpu scale-down-gpu clean

help:
	@echo "Bootstrap OpenShift Cluster for LlamaStack Demo"
	@echo ""
	@echo "Available targets:"
	@echo "  install-deps      - Install required Ansible collections"
	@echo "  bootstrap         - Run the bootstrap playbook"
	@echo "  bootstrap-verbose - Run bootstrap with verbose output"
	@echo "  check-cluster     - Verify cluster access and status"
	@echo "  scale-up-gpu      - Scale GPU nodes to 1 replica"
	@echo "  scale-down-gpu    - Scale GPU nodes to 0 (cost saving)"
	@echo "  clean             - Remove generated Ansible artifacts"
	@echo ""
	@echo "Example usage:"
	@echo "  make install-deps && make bootstrap"

install-deps:
	@echo "Installing Ansible collection dependencies..."
	ansible-galaxy collection install -r requirements.yml

bootstrap: install-deps
	@echo "Running bootstrap playbook..."
	ansible-playbook bootstrap.yml

bootstrap-verbose: install-deps
	@echo "Running bootstrap playbook (verbose)..."
	ansible-playbook bootstrap.yml -vv

check-cluster:
	@echo "Checking OpenShift cluster status..."
	@echo "Cluster user:"
	@oc whoami
	@echo ""
	@echo "OpenShift version:"
	@oc version | head -1
	@echo ""
	@echo "OpenShift AI CSV:"
	@oc get csv -n redhat-ods-operator | grep rhods-operator || echo "OpenShift AI not found"
	@echo ""
	@echo "GPU machinesets:"
	@oc get machineset -n openshift-machine-api | grep gpu || echo "No GPU machinesets found"

scale-up-gpu:
	@echo "Scaling GPU nodes to 1 replica..."
	@oc scale $$(oc get machineset -n openshift-machine-api -o name | grep gpu) --replicas=1 -n openshift-machine-api
	@echo "Waiting for nodes to be ready (this may take several minutes)..."
	@oc wait --for=condition=Ready node -l node-role.kubernetes.io/worker --timeout=10m || true

scale-down-gpu:
	@echo "Scaling GPU nodes to 0 replicas (cost saving)..."
	@oc scale $$(oc get machineset -n openshift-machine-api -o name | grep gpu) --replicas=0 -n openshift-machine-api
	@echo "GPU nodes will terminate shortly."

clean:
	@echo "Cleaning up Ansible artifacts..."
	@rm -rf ~/.ansible/collections/ansible_collections/kubernetes
	@rm -rf ~/.ansible/collections/ansible_collections/community
	@echo "Clean complete."
