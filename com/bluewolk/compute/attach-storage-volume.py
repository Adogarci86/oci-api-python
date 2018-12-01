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

instance_id = sys.argv[1].replace('\n','')
volume_id = sys.argv[2].replace('\n','')

request = oci.core.models.attach_i_scsi_volume_details.AttachIScsiVolumeDetails()
request.compartment_id = compartment_id
request.instance_id = instance_id
request.volume_id = volume_id

compute = oci.core.compute_client.ComputeClient( config )
response = compute.attach_volume( request )

assert response.status == 200
assert type(response.data) is oci.core.models.IScsiVolumeAttachment

response = compute.get_volume_attachment( response.data.id )
attachment = oci.wait_until( compute, response, 'lifecycle_state', 'ATTACHED').data

print (attachment.ipv4)

