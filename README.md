# toolbus
Provides Hosts with a new configuration (IP, hostname, DNS, ssh keys, ...) based on hostname.
I created some VM templates that needed their own configuration before joining a cluster.
A Server providing all configuration data and a setup script that is run on the host.

## Flow
Host powers on and asks the server for it's config. If the host is new to the cluster it gets 
a new config depending on its role inside the cluster. The role is determined by the hostname 
given to the template. After setup the host joins the cluster (rke, k8s, ..). If the host already 
exists in the database the setup restarts at the next stage.

## Requirements
The host needs 
* an initial working network configuration (some standard cloud-init, dhcp, ..)
* python to execute the setup script
* a hostname to define its role in the cluster (cluster**etcd**, cluster**worker**, ..)
