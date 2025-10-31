# GPU Scaling Automation

Automated GPU node scaling to reduce costs when the demo cluster is not in use.

## Overview

GPU instances are expensive (~$1.50/hour for g6e.2xlarge). This automation scales down GPU nodes during off-hours and scales them back up during business hours to save money.

## Schedule

- **Scale UP**: 8 AM EST (1 PM UTC) Monday-Friday
- **Scale DOWN**: 6 PM EST (11 PM UTC) Monday-Friday

**Cost Savings**: ~10 hours/day × 5 days/week = **~50 hours/week saved** (~$75/week for 1 GPU node)

## Components

### CronJobs

1. **[gpu-scale-down-cronjob.yml](gpu-scale-down-cronjob.yml)**
   - Runs at 6 PM EST weekdays
   - Scales GPU MachineSets to 0 replicas
   - Finds MachineSets by label `agnosticd.redhat.com/machineset-group=worker-gpu`
   - Fallback: searches by name pattern `gpu`

2. **[gpu-scale-up-cronjob.yml](gpu-scale-up-cronjob.yml)**
   - Runs at 8 AM EST weekdays
   - Scales GPU MachineSets to 1 replica
   - Same discovery logic as scale-down

### RBAC

- **ServiceAccount**: `gpu-scaler` in `openshift-machine-api` namespace
- **Permissions**: Read/write access to MachineSets and Machines in `openshift-machine-api` namespace

## Deployment

```bash
# Deploy GPU scaling automation
oc apply -k demo/components/developer-tools/automation/

# Verify CronJobs are created
oc get cronjobs -n openshift-machine-api

# Check schedule
oc get cronjobs -n openshift-machine-api -o wide
```

## Manual Scaling

You can still manually scale GPU nodes when needed:

```bash
# Scale down immediately
oc create job manual-scale-down --from=cronjob/gpu-scale-down -n openshift-machine-api

# Scale up immediately
oc create job manual-scale-up --from=cronjob/gpu-scale-up -n openshift-machine-api

# Or use oc scale directly
oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) --replicas=0 -n openshift-machine-api
oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) --replicas=1 -n openshift-machine-api
```

## Monitoring

```bash
# View recent Jobs
oc get jobs -n openshift-machine-api -l app=gpu-scaling-automation

# Check Job logs
oc logs -n openshift-machine-api -l app=gpu-scaling-automation --tail=50

# View CronJob history
oc get jobs -n openshift-machine-api -l operation=scale-down
oc get jobs -n openshift-machine-api -l operation=scale-up

# Check current GPU MachineSets state
oc get machinesets -n openshift-machine-api | grep gpu
```

## Customizing the Schedule

Edit the CronJob schedule field (uses standard cron syntax in UTC):

```yaml
spec:
  # Current: 6 PM EST = 11 PM UTC (scale down)
  schedule: "0 23 * * 1-5"

  # Examples:
  # 5 PM EST weekdays: "0 22 * * 1-5"
  # 7 PM EST weekdays: "0 0 * * 1-5"
  # Every day: "0 23 * * *"
```

**Note**: OpenShift uses UTC. EST = UTC-5, EDT = UTC-4. Adjust accordingly.

## Disabling Automation

```bash
# Suspend CronJobs (stop automatic scaling)
oc patch cronjob gpu-scale-down -n openshift-machine-api -p '{"spec":{"suspend":true}}'
oc patch cronjob gpu-scale-up -n openshift-machine-api -p '{"spec":{"suspend":true}}'

# Resume CronJobs
oc patch cronjob gpu-scale-down -n openshift-machine-api -p '{"spec":{"suspend":false}}'
oc patch cronjob gpu-scale-up -n openshift-machine-api -p '{"spec":{"suspend":false}}'

# Delete automation entirely
oc delete -k demo/components/developer-tools/automation/
```

## Troubleshooting

### CronJob Not Running

Check if the CronJob is suspended:
```bash
oc get cronjob gpu-scale-down -n openshift-machine-api -o jsonpath='{.spec.suspend}'
```

### Permission Errors

Verify RBAC is configured:
```bash
oc get serviceaccount gpu-scaler -n openshift-machine-api
oc get role gpu-scaler -n openshift-machine-api
oc get rolebinding gpu-scaler -n openshift-machine-api
```

### MachineSets Not Found

The CronJobs try two discovery methods:
1. Label: `agnosticd.redhat.com/machineset-group=worker-gpu`
2. Name pattern: contains `gpu`

Verify your GPU MachineSets match one of these:
```bash
oc get machinesets -n openshift-machine-api -l agnosticd.redhat.com/machineset-group=worker-gpu
oc get machinesets -n openshift-machine-api | grep gpu
```

If neither works, you may need to update the CronJob scripts to match your MachineSets.

### GPU Pods Stuck After Scale-Up

GPU nodes take 5-10 minutes to provision and become Ready. Check node status:
```bash
# Watch GPU nodes
oc get nodes -l node-role.kubernetes.io/worker-gpu -w

# Check if pods are waiting for GPU
oc get pods -n summit-connect-2025 -o wide | grep Pending
```

## Cost Estimation

Assuming AWS g6e.2xlarge ($1.50/hour):

- **Without automation**: 24h × 7 days = 168 hours/week = **$252/week**
- **With automation**: 10h × 5 days = 50 hours/week = **$75/week**
- **Savings**: **$177/week** (~70% reduction) or **~$707/month**

Adjust numbers based on your actual GPU instance type and pricing.

## Important Notes

- **Weekends**: Automation runs Monday-Friday only. GPU nodes stay in whatever state they were in on Friday evening.
- **Holidays**: CronJobs still run on holidays (Monday-Friday). Manually suspend if needed.
- **Demo Timing**: If demoing outside of 8 AM - 6 PM EST, manually scale up beforehand.
- **Model Loading**: After scale-up, models take ~2-3 minutes to load in addition to node provisioning time.
- **Data Persistence**: PVCs and model data persist when GPU nodes are scaled down.

## Best Practices

1. **Before a Demo**:
   ```bash
   # Ensure GPU nodes are up
   oc get nodes -l node-role.kubernetes.io/worker-gpu

   # If not, manually scale up
   oc create job manual-scale-up --from=cronjob/gpu-scale-up -n openshift-machine-api
   ```

2. **After Hours Work**:
   If working late, suspend scale-down:
   ```bash
   oc patch cronjob gpu-scale-down -n openshift-machine-api -p '{"spec":{"suspend":true}}'
   ```

3. **Extended Downtime**:
   If cluster won't be used for weeks, manually scale down:
   ```bash
   oc scale $(oc get machineset -n openshift-machine-api -o name | grep gpu) --replicas=0 -n openshift-machine-api
   ```
