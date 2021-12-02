Push new versions of containers

oc scale --replicas=2 deployment/sui-demo
oc delete pods <old_pod_name>
oc scale --replicas=1 deployment/sui-demo