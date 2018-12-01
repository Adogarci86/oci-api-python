'''
Created on Nov 30, 2018

@author: adogarci
'''
import oci
import os
import time
import sys

config = oci.config.from_file("~/.oci/config")
compartment_id = config["compartment"]
vcn_id = config["vcn"]

volume_size = int(sys.argv[1])
volume_name = str(sys.argv[2])
availability_domain = str(sys.argv[3])

request = oci.core.models.create_volume_details.CreateVolumeDetails()
request.display_name = volume_name
request.compartment_id = compartment_id
request.availability_domain = availability_domain
request.size_in_gbs = volume_size


block_storage = oci.core.blockstorage_client.BlockstorageClient( config )
response = block_storage.create_volume(request, opc_retry_token='testtoken{}'.format(int(time.time())))

assert response.status == 200
assert type(response.data) is oci.core.models.Volume

response = block_storage.get_volume( response.data.id )
volume = oci.wait_until( block_storage, response, 'lifecycle_state', 'AVAILABLE', max_wait_seconds=180).data

print (volume.id)