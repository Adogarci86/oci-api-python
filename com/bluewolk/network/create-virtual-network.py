'''
Created on Nov 30, 2018

@author: adogarci
'''
import oci
import os
import time

config = oci.config.from_file("~/.oci/config")
compartment_id = config["compartment"]

print('Creating Cloud Network')

vcn_id = "blackwolk_sdk_vnc"

request = oci.core.models.create_vcn_details.CreateVcnDetails()
request.cidr_block = '10.67.0.0/16'
request.display_name = 'blackwolk_sdk_vnc'
request.compartment_id = compartment_id
request.vcn_id = vcn_id

vcn = oci.core.virtual_network_client.VirtualNetworkClient( config )
response = vcn.create_vcn( request )

assert response.status == 200
assert type(response.data) is oci.core.models.Vcn

response = vcn.get_vcn(response.data.id)

virtualcn = oci.wait_until(vcn, response, 'lifecycle_state', 'AVAILABLE').data
print (str(virtualcn.id))

assert 'AVAILABLE' == virtualcn.lifecycle_state
print(str(virtualcn))
print ('VCN created!!!')