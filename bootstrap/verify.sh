#!/bin/bash
# Quick verification script for cluster prerequisites

set -e

echo "========================================="
echo "OpenShift Cluster Verification"
echo "========================================="
echo ""

# Check oc CLI
echo "✓ Checking oc CLI..."
if ! command -v oc &> /dev/null; then
    echo "✗ ERROR: oc CLI not found. Please install it first."
    exit 1
fi
echo "  $(oc version --client | head -1)"
echo ""

# Check cluster access
echo "✓ Checking cluster access..."
if ! oc whoami &> /dev/null; then
    echo "✗ ERROR: Not logged into OpenShift. Run 'oc login' first."
    exit 1
fi
echo "  Logged in as: $(oc whoami)"
echo "  Cluster: $(oc whoami --show-server)"
echo ""

# Check OpenShift AI
echo "✓ Checking OpenShift AI installation..."
RHODS_CSV=$(oc get csv -n redhat-ods-operator 2>/dev/null | grep rhods-operator | awk '{print $1}' || echo "")
if [ -z "$RHODS_CSV" ]; then
    echo "✗ ERROR: OpenShift AI operator not installed."
    echo "  Please install it via OperatorHub first."
    exit 1
fi
echo "  Current version: $RHODS_CSV"

# Check version
if [[ $RHODS_CSV == *"2.23.0"* ]]; then
    echo "  ✓ Already on target version 2.23.0"
else
    echo "  ⚠ Upgrade needed to 2.23.0"
fi
echo ""

# Check LlamaStack operator
echo "✓ Checking LlamaStack operator..."
LLAMASTACK_ENABLED=$(oc get datasciencecluster default-dsc -o jsonpath='{.spec.components.llamastack.managementState}' 2>/dev/null || echo "")
if [ "$LLAMASTACK_ENABLED" = "Managed" ]; then
    echo "  ✓ LlamaStack operator is enabled"
else
    echo "  ⚠ LlamaStack operator not enabled (will be configured)"
fi
echo ""

# Check GPU operators
echo "✓ Checking GPU operators..."
NFD_INSTALLED=$(oc get subscription nfd -n openshift-nfd 2>/dev/null && echo "yes" || echo "no")
NVIDIA_INSTALLED=$(oc get subscription -n nvidia-gpu-operator 2>/dev/null | grep -q nvidia && echo "yes" || echo "no")

if [ "$NFD_INSTALLED" = "yes" ]; then
    echo "  ✓ Node Feature Discovery operator installed"
else
    echo "  ✗ Node Feature Discovery operator NOT installed"
fi

if [ "$NVIDIA_INSTALLED" = "yes" ]; then
    echo "  ✓ NVIDIA GPU operator installed"
else
    echo "  ✗ NVIDIA GPU operator NOT installed"
fi

if [ "$NFD_INSTALLED" = "no" ] || [ "$NVIDIA_INSTALLED" = "no" ]; then
    echo "  ⚠ GPU operators required for model serving. Install via OperatorHub."
fi
echo ""

# Check GPU machinesets
echo "✓ Checking GPU machinesets..."
GPU_MACHINESETS=$(oc get machineset -n openshift-machine-api -o name 2>/dev/null | grep gpu || echo "")
if [ -z "$GPU_MACHINESETS" ]; then
    echo "  ⚠ No GPU machinesets found"
    echo "    Models will not be able to schedule without GPU nodes"
else
    for ms in $GPU_MACHINESETS; do
        REPLICAS=$(oc get $ms -n openshift-machine-api -o jsonpath='{.spec.replicas}')
        echo "  $ms: $REPLICAS replicas"
    done
fi
echo ""

# Check namespace
echo "✓ Checking demo namespace..."
if oc get namespace summit-connect-2025 &>/dev/null; then
    echo "  ✓ Namespace 'summit-connect-2025' exists"
else
    echo "  ⚠ Namespace 'summit-connect-2025' will be created"
fi
echo ""

# Check Ansible
echo "✓ Checking Ansible installation..."
if command -v ansible-playbook &> /dev/null; then
    ANSIBLE_VERSION=$(ansible-playbook --version | head -1)
    echo "  ✓ $ANSIBLE_VERSION"
else
    echo "  ⚠ Ansible not found. Install with: pip install ansible"
    echo ""
    echo "========================================="
    echo "Verification Complete (with warnings)"
    echo "========================================="
    exit 1
fi
echo ""

echo "========================================="
echo "✓ Verification Complete!"
echo "========================================="
echo ""
echo "Ready to run bootstrap:"
echo "  make bootstrap"
echo ""
