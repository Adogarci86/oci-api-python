'''
Created on Nov 30, 2018

@author: adogarci
'''
import oci
import os
import time
import json

config = oci.config.from_file("~/.oci/config")
compartment_id = config["compartment"]
vcn_id = config["vcn"]

vcn = oci.core.virtual_network_client.VirtualNetworkClient( config )
compute = oci.core.compute_client.ComputeClient( config )
instances = compute.list_instances(compartment_id)

assert instances.status == 200
assert len(instances.data) > 0

attachments = compute.list_vnic_attachments( compartment_id )

assert attachments.status == 200
assert len(attachments.data) > 0


out = {'group': {'hosts': {}}, '_meta': {'hostvars': {}}}

ips = []

for instance in instances.data:
    if 'RUNNING' in str(instance.lifecycle_state):
        id = str(instance.id)
        vnic_attachment = next(va for va in attachments.data if va.instance_id == id)
        vnic = vcn.get_vnic(vnic_attachment.vnic_id)
        ips.append(str(vnic.data.private_ip))
        out['_meta']['hostvars'][instance.display_name] = {
            'oci_hosts': instance.display_name,
            'oci_public_ip': vnic.data.public_ip,
            'oci_private_ip': vnic.data.private_ip,
        }

out['group']['hosts'] = ips

print(json.dumps(out, indent=4, sort_keys=False))
