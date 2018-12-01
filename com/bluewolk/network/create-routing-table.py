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
gateway_id = config["gateway"]

print('Updating Route Table')

route_rule = oci.core.models.RouteRule()
route_rule.cidr_block = '0.0.0.0/0'
route_rule.display_name = 'blackwolk_route_rule'
route_rule.network_entity_id = gateway_id
route_rule.network_entity_type = 'INTERNET_GATEWAY' 

request = oci.core.models.update_route_table_details.UpdateRouteTableDetails()
request.route_rules = [route_rule]

vcn = oci.core.virtual_network_client.VirtualNetworkClient( config )

response = vcn.update_route_table( routing_id, request )

assert response.status == 200
assert type(response.data) is oci.core.models.RouteTable

response = vcn.get_route_table( routing_id )

virtualcn = oci.wait_until(vcn, response, 'lifecycle_state', 'AVAILABLE').data

assert 'AVAILABLE' == virtualcn.lifecycle_state
print (str(virtualcn))

print ('Route Table Updated!!!')