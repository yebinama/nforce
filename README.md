# Nforce Neutron Agent Extension

The goal of this extension is to enforce security groups on all VMs. Whenever a port is modified, it will check if mandatory security groups are missing and will enforce them if needed.

To use this extension, you first need to create the security groups that you want to share in a specific project id, tag them with a custom tag and share them with a rbac rule.

Example:
``` sh
openstack security group create mandatory_sg --tag infra
openstack network rbac create --type security_group --action access_as_shared --target-all-projects mandatory_sg
```

## Installation

In order to use this extension, you need to install and configure it on your hypervisor nodes (container neutron_openvswitch_agent when using kolla-ansible).

- Install the nforce package by executing the following command:

``` sh
 pip install .
```

## Configuration

Open the Neutron Openvswitch configuration file named `openvswitch_agent.ini`.

- Under the `[agent]` section, add Nforce extension to the `extensions` list.

```shell
[agent]
...
extensions = nforce
```

- Finally, under the `[nforce]` section,  add the location of the configuration file

```shell
[nforce]
config_file = /etc/neutron/plugins/ml2/nforce.ini
```

# Configuration file

Here is an example of a detailed configuration file

```shell
[nforce]
# Security Groups tag to look for.
tag = infra
# Project id in which the security groups are defined.
project_id = 1987981eff3f4cf7bf6335a5f0d2f82b
# TTL for requesting mandatory security groups.
ttl = 30
# Number of retries for OpenStack requests.
retries = 3

# OpenStack connection configuration (see Octavia configuration)
[openstack]
auth_url =
auth_type =
username =
password =
user_domain_name =
project_name =
project_domain_name =
cafile =
region_name =

[neutron]
region_name = RegionOne
endpoint_type = internal
ca_certificates_file =
```
