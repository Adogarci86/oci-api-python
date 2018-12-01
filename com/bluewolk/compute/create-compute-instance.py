'''
Created on Nov 30, 2018

@author: adogarci
'''
import oci
import os
import time
import subprocess
import sys

instance_name = sys.argv[1]
oci_shape = sys.argv[2]
oci_subnet_id = sys.argv[3]
availability_domain = sys.argv[4]
linux_image_id = sys.argv[5]

config = oci.config.from_file("~/.oci/config")
compartment_id = config["compartment"]
vcn_id = config["vcn"]
subnet_id = config[oci_subnet_id]
linux_image = config[linux_image_id]
ssh_key = config["ssh_key"]

with open(ssh_key) as key_file:
    public_key = key_file.read().strip()

request = oci.core.models.launch_instance_details.LaunchInstanceDetails()
request.availability_domain = availability_domain
request.compartment_id = compartment_id
request.display_name = instance_name
request.image_id = linux_image
request.shape = oci_shape
request.subnet_id = subnet_id
request.metadata = {'ssh_authorized_keys': public_key}

compute = oci.core.compute_client.ComputeClient( config )

response = compute.launch_instance( request )

assert response.status == 200
assert 'PROVISIONING' == response.data.lifecycle_state

response = compute.get_instance( response.data.id )

instance = oci.wait_until(compute, response, 'lifecycle_state', 'RUNNING', max_wait_secons=300).data

assert 'RUNNING' == instance.lifecycle_state

response = compute.list_vnic_attachments( compartment_id )

assert response.status == 200
assert len(response.data) > 0

vnic_attachment = next(va for va in response.data if va.instance_id == instance.id)

vcn = oci.core.virtual_network_client.VirtualNetworkClient( config )
response = vcn.get_vnic(vnic_attachment.vnic_id)

response = oci.wait_until( vcn, response, 'lifecycle_state', 'AVAILABLE' )

assert response.status == 200
assert response.data.public_ip is not None

print (str(instance.id))