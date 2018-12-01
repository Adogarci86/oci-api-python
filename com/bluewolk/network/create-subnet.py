'''
Created on Nov 30, 2018

@author: adogarci
'''
import oci
import os
import time

config = oci.config.from_file("~/.oci/config")
compartment_id = config["compartment"]
vcn_id = config["vcn"]
routing_id = config["route"]

print('Creating Cloud Subnet')

request = oci.core.models.create_subnet_details.CreateSubnetDetails()
request.cidr_block = '10.67.1.0/24'
request.availability_domain = 'KeeS:US-ASHBURN-AD-1'
request.display_name = 'blackwolk_sdk_subnet'
request.compartment_id = compartment_id
request.route_table_id = routing_id
request.vcn_id = vcn_id

vcn = oci.core.virtual_network_client.VirtualNetworkClient( config )

response = vcn.create_subnet( request )

assert response.status == 200
assert type(response.data) is oci.core.models.Subnet

response = vcn.get_subnet(response.data.id)

virtualcn = oci.wait_until(vcn, response, 'lifecycle_state', 'AVAILABLE').data
print (str(virtualcn.id))

assert 'AVAILABLE' == virtualcn.lifecycle_state
print (str(virtualcn))

print ('Subnet created!!!')