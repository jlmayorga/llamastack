#!/bin/bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default action
ACTION=""

# Default replica counts
WORKER_REPLICAS=${WORKER_REPLICAS:-2}
GPU_REPLICAS=${GPU_REPLICAS:-1}

# Login credentials (prefer environment variables for security)
OC_SERVER=${OC_SERVER:-""}
OC_USERNAME=${OC_USERNAME:-""}
OC_PASSWORD=${OC_PASSWORD:-""}
SKIP_LOGIN=${SKIP_LOGIN:-false}

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Cleanup function
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Script failed with exit code $exit_code"
    fi
}

trap cleanup EXIT

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        up|down)
            ACTION="$1"
            shift
            ;;
        --workers)
            if ! [[ "$2" =~ ^[0-9]+$ ]]; then
                log_error "Worker replicas must be a positive integer"
                exit 1
            fi
            WORKER_REPLICAS="$2"
            shift 2
            ;;
        --gpu)
            if ! [[ "$2" =~ ^[0-9]+$ ]]; then
                log_error "GPU replicas must be a positive integer"
                exit 1
            fi
            GPU_REPLICAS="$2"
            shift 2
            ;;
        --server)
            OC_SERVER="$2"
            shift 2
            ;;
        --username)
            OC_USERNAME="$2"
            shift 2
            ;;
        --password)
            OC_PASSWORD="$2"
            shift 2
            ;;
        --skip-login)
            SKIP_LOGIN=true
            shift
            ;;
        -h|--help)
            cat << EOF
Usage: $0 <up|down> [OPTIONS]

Actions:
  up      Scale up the cluster (default: 2 workers, 1 GPU)
  down    Scale down the cluster (default: 0 workers, 0 GPU)

Options:
  --workers <num>      Number of worker node replicas
  --gpu <num>          Number of GPU node replicas
  --server <url>       OpenShift server URL (or set OC_SERVER env var)
  --username <user>    OpenShift username (or set OC_USERNAME env var)
  --password <pass>    OpenShift password (or set OC_PASSWORD env var)
  --skip-login         Skip login if already authenticated
  -h, --help           Show this help message

Environment Variables (recommended for credentials):
  OC_SERVER            OpenShift server URL
  OC_USERNAME          OpenShift username
  OC_PASSWORD          OpenShift password
  WORKER_REPLICAS      Default worker replicas for scale up
  GPU_REPLICAS         Default GPU replicas for scale up
  SKIP_LOGIN           Set to 'true' to skip login

Examples:
  # Scale up with defaults (2 workers, 1 GPU)
  $0 up --server https://api.cluster.example.com:6443 --username admin --password secret

  # Using environment variables (more secure)
  export OC_SERVER=https://api.cluster.example.com:6443
  export OC_USERNAME=admin
  export OC_PASSWORD=secret
  $0 up

  # Scale down everything
  $0 down

  # Custom scale up
  $0 up --workers 3 --gpu 2

  # If already logged in
  $0 up --skip-login

Security Note:
  Passing passwords via command line is insecure. Use environment variables instead:
  export OC_PASSWORD='your-password'
  $0 up --server ... --username ...

EOF
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Validate action
if [ -z "$ACTION" ]; then
    log_error "Action required (up or down)"
    echo "Use --help for usage information"
    exit 1
fi

# Set defaults based on action
if [ "$ACTION" = "down" ]; then
    # Override defaults for scale-down unless explicitly set via command line
    if [ "${WORKER_REPLICAS}" = "2" ]; then
        WORKER_REPLICAS=0
    fi
    if [ "${GPU_REPLICAS}" = "1" ]; then
        GPU_REPLICAS=0
    fi
fi

# Login to OpenShift cluster
if [ "$SKIP_LOGIN" != "true" ]; then
    log_info "Checking OpenShift authentication..."

    # Check if already logged in
    if oc whoami &>/dev/null; then
        CURRENT_USER=$(oc whoami)
        CURRENT_SERVER=$(oc whoami --show-server)
        log_info "Already logged in as ${CURRENT_USER} to ${CURRENT_SERVER}"

        # If credentials provided, verify they match
        if [ -n "$OC_SERVER" ] && [ "$CURRENT_SERVER" != "$OC_SERVER" ]; then
            log_warn "Currently connected to different server. Logging in to ${OC_SERVER}..."
        elif [ -n "$OC_USERNAME" ] && [ "$CURRENT_USER" != "$OC_USERNAME" ]; then
            log_warn "Currently logged in as different user. Switching to ${OC_USERNAME}..."
        else
            log_info "Using existing session"
            OC_SERVER="$CURRENT_SERVER"
        fi
    fi

    # Login if credentials provided or if server/user mismatch
    if [ -n "$OC_SERVER" ] && [ -n "$OC_USERNAME" ] && [ -n "$OC_PASSWORD" ]; then
        log_info "Logging in to OpenShift cluster..."
        if ! oc login "$OC_SERVER" -u "$OC_USERNAME" -p "$OC_PASSWORD" --insecure-skip-tls-verify=true; then
            log_error "Failed to login to OpenShift cluster"
            exit 1
        fi
        log_info "Successfully logged in as ${OC_USERNAME}"
    elif ! oc whoami &>/dev/null; then
        log_error "Not logged in to OpenShift. Provide credentials or use --skip-login if already authenticated"
        echo "Use --help for more information"
        exit 1
    fi
else
    log_info "Skipping login check as requested"
    if ! oc whoami &>/dev/null; then
        log_error "Not authenticated to OpenShift cluster"
        exit 1
    fi
fi

# Verify cluster access
log_info "Verifying cluster access..."
if ! oc get machinesets -n openshift-machine-api &>/dev/null; then
    log_error "Cannot access machinesets. Check permissions for user $(oc whoami)"
    exit 1
fi

echo ""
echo "========================================"
ACTION_DISPLAY=$(echo "$ACTION" | tr '[:lower:]' '[:upper:]')
echo "OpenShift Cluster Scale ${ACTION_DISPLAY}"
echo "========================================"
echo "Server:       $(oc whoami --show-server)"
echo "User:         $(oc whoami)"
echo "Configuration:"
echo "  Worker nodes: ${WORKER_REPLICAS} replicas"
echo "  GPU nodes:    ${GPU_REPLICAS} replicas"
echo "========================================"
echo ""

# Get current machineset status
log_info "[1/4] Checking current machineset status..."
oc get machinesets -n openshift-machine-api
echo ""

# Scale worker nodes
log_info "[2/4] Scaling worker machinesets to ${WORKER_REPLICAS} replicas..."
WORKER_MACHINESETS=$(oc get machineset -n openshift-machine-api -o name | grep worker | grep -v gpu || true)
if [ -z "$WORKER_MACHINESETS" ]; then
    log_error "No worker machinesets found!"
    exit 1
fi

echo "Found worker machinesets:"
echo "$WORKER_MACHINESETS"
echo ""

for ms in $WORKER_MACHINESETS; do
    log_info "Scaling ${ms} to ${WORKER_REPLICAS} replicas..."
    if ! oc scale "$ms" --replicas="$WORKER_REPLICAS" -n openshift-machine-api; then
        log_error "Failed to scale ${ms}"
        exit 1
    fi
done
log_info "✓ Worker machinesets scaled"
echo ""

# Scale GPU nodes
log_info "[3/4] Scaling GPU machinesets to ${GPU_REPLICAS} replicas..."
GPU_MACHINESETS=$(oc get machineset -n openshift-machine-api -o name | grep gpu || true)
GPU_COUNT=0

if [ -z "$GPU_MACHINESETS" ]; then
    log_warn "No GPU machinesets found, skipping..."
else
    echo "Found GPU machinesets:"
    echo "$GPU_MACHINESETS"
    echo ""

    GPU_COUNT=$(echo "$GPU_MACHINESETS" | wc -l | tr -d '[:space:]')
    for ms in $GPU_MACHINESETS; do
        log_info "Scaling ${ms} to ${GPU_REPLICAS} replicas..."
        if ! oc scale "$ms" --replicas="$GPU_REPLICAS" -n openshift-machine-api; then
            log_error "Failed to scale ${ms}"
            exit 1
        fi
    done
    log_info "✓ GPU machinesets scaled"
fi
echo ""

if [ "$ACTION" = "up" ]; then
    # Wait for machines to be created and nodes to be ready
    log_info "[4/4] Waiting for machines to be provisioned..."
    sleep 5

    WORKER_COUNT=$(echo "$WORKER_MACHINESETS" | wc -l | tr -d '[:space:]')
    EXPECTED_MACHINES=$(( (WORKER_COUNT * WORKER_REPLICAS) + (GPU_COUNT * GPU_REPLICAS) ))
    log_info "Expecting ${EXPECTED_MACHINES} worker/GPU machines total"

    TIMEOUT=600  # 10 minutes
    ELAPSED=0

    while [ $ELAPSED -lt $TIMEOUT ]; do
        RUNNING_MACHINES=$(oc get machines -n openshift-machine-api --no-headers 2>/dev/null | grep -v "master\|control-plane" | grep -c "Running" || echo "0")
        RUNNING_MACHINES=$(echo "$RUNNING_MACHINES" | tr -d '[:space:]')
        TOTAL_MACHINES=$(oc get machines -n openshift-machine-api --no-headers 2>/dev/null | grep -v "master\|control-plane" | wc -l | tr -d '[:space:]')

        echo "⏳ Machines status: ${RUNNING_MACHINES}/${TOTAL_MACHINES} running (expecting ${EXPECTED_MACHINES} total)"

        if [ "$TOTAL_MACHINES" -ge "$EXPECTED_MACHINES" ]; then
            log_info "✓ All machines created!"
            break
        fi

        sleep 10
        ELAPSED=$((ELAPSED + 10))
    done

    if [ $ELAPSED -ge $TIMEOUT ]; then
        log_warn "Timeout waiting for all machines to be created"
    fi
    echo ""

    # Wait for nodes to be Ready
    log_info "Waiting for nodes to be Ready..."
    TIMEOUT=900  # 15 minutes
    ELAPSED=0

    while [ $ELAPSED -lt $TIMEOUT ]; do
        READY_NODES=$(oc get nodes --no-headers 2>/dev/null | grep -v "master\|control-plane" | grep -c " Ready" || echo "0")
        READY_NODES=$(echo "$READY_NODES" | tr -d '[:space:]')
        TOTAL_NODES=$(oc get nodes --no-headers 2>/dev/null | grep -v "master\|control-plane" | wc -l | tr -d '[:space:]')

        echo "⏳ Nodes status: ${READY_NODES}/${TOTAL_NODES} ready"

        # Show individual node status
        echo "Current node status:"
        oc get nodes -o wide 2>/dev/null | grep -E "NAME|worker|gpu" || true
        echo ""

        # Check if all nodes are Ready
        NOT_READY=$(oc get nodes --no-headers 2>/dev/null | grep -v "master\|control-plane" | grep -c "NotReady" || echo "0")
        NOT_READY=$(echo "$NOT_READY" | tr -d '[:space:]')

        if [ "$NOT_READY" -eq 0 ] && [ "$TOTAL_NODES" -ge "$EXPECTED_MACHINES" ]; then
            log_info "✓ All nodes are Ready!"
            break
        fi

        sleep 15
        ELAPSED=$((ELAPSED + 15))
    done

    if [ $ELAPSED -ge $TIMEOUT ]; then
        log_warn "Timeout waiting for all nodes to be Ready"
        echo "Current status:"
        oc get nodes
        exit 1
    fi

else
    # Scale down - wait for machines to be deleted
    log_info "[4/4] Waiting for machines to be terminated..."
    sleep 5

    TIMEOUT=600  # 10 minutes
    ELAPSED=0

    WORKER_COUNT=$(echo "$WORKER_MACHINESETS" | wc -l | tr -d '[:space:]')
    EXPECTED_MACHINES=$(( (WORKER_COUNT * WORKER_REPLICAS) + (GPU_COUNT * GPU_REPLICAS) ))
    log_info "Expecting ${EXPECTED_MACHINES} worker/GPU machines to remain"

    while [ $ELAPSED -lt $TIMEOUT ]; do
        TOTAL_MACHINES=$(oc get machines -n openshift-machine-api --no-headers 2>/dev/null | grep -v "master\|control-plane" | wc -l | tr -d '[:space:]')
        DELETING_MACHINES=$(oc get machines -n openshift-machine-api --no-headers 2>/dev/null | grep -v "master\|control-plane" | grep -c "Deleting" || echo "0")
        DELETING_MACHINES=$(echo "$DELETING_MACHINES" | tr -d '[:space:]')

        echo "⏳ Machines status: ${TOTAL_MACHINES} total, ${DELETING_MACHINES} deleting (target: ${EXPECTED_MACHINES})"

        if [ "$TOTAL_MACHINES" -le "$EXPECTED_MACHINES" ] && [ "$DELETING_MACHINES" -eq 0 ]; then
            log_info "✓ Machines scaled down!"
            break
        fi

        # Show machines being deleted
        echo "Current machines:"
        oc get machines -n openshift-machine-api 2>/dev/null | grep -E "NAME|worker|gpu" || true
        echo ""

        sleep 10
        ELAPSED=$((ELAPSED + 10))
    done

    if [ $ELAPSED -ge $TIMEOUT ]; then
        log_warn "Timeout waiting for machines to be deleted"
    fi
fi

echo ""
echo "========================================"
log_info "✓ Cluster scale ${ACTION} complete!"
echo "========================================"
echo ""
echo "Final status:"
oc get machinesets -n openshift-machine-api
echo ""
oc get nodes -o wide
echo ""

if [ "$ACTION" = "up" ]; then
    echo "All systems ready! 🚀"
else
    echo "Cluster scaled down! 💤"
fi

exit 0