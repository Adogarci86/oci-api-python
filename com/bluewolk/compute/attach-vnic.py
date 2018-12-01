'''
Created on Nov 30, 2018

@author: adogarci
'''
import oci
import os
import time
import subprocess
import sys

config = oci.config.from_file("~/.oci/config")
compartment_id = config["compartment"]
vcn_id = config["vcn"]
ssh_key = config["ssh_key"]

instance_id = sys.argv[1].replace('\n','')

compute = oci.core.compute_client.ComputeClient( config )

response = compute.list_vnic_attachments( compartment_id )

assert response.status == 200
assert len(response.data) > 0

vnic_attachment = next(va for va in response.data if va.instance_id == instance_id)

vcn = oci.core.virtual_network_client.VirtualNetworkClient( config )
response = vcn.get_vnic(vnic_attachment.vnic_id)

response = oci.wait_until( vcn, response, 'lifecycle_state', 'AVAILABLE' )

assert response.status == 200
assert response.data.private_ip is not None

print (str(response.data.private_ip))

