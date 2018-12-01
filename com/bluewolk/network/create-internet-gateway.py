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

print('Creating Internet Gateway')

request = oci.core.models.create_internet_gateway_details.CreateInternetGatewayDetails()
request.display_name = 'blackwolk_internet_gateway'
request.compartment_id = compartment_id
request.is_enabled = True
request.vcn_id = vcn_id

vcn = oci.core.virtual_network_client.VirtualNetworkClient( config )

response = vcn.create_internet_gateway( request )

assert response.status == 200
assert type(response.data) is oci.core.models.InternetGateway

response = vcn.get_internet_gateway(response.data.id)

virtualcn = oci.wait_until(vcn, response, 'lifecycle_state', 'AVAILABLE').data
print (str(virtualcn.id))

assert 'AVAILABLE' == virtualcn.lifecycle_state
print (str(virtualcn))

print ('Internet Gateway created!!!')