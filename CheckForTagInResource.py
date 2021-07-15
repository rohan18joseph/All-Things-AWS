import boto3 
import json

client = boto3.client('resourcegroupstaggingapi') #initializing client

paginator = client.get_paginator('get_resources') #setting up a paginator since get_resources() is a paginating call.
pages= paginator.paginate()
for page in pages:
    resources=page['ResourceTagMappingList']
    for resource in resources: #iterating across all the resources in the 'page'
        flag=0 #flag set to 0
        tags=resource['Tags'] 
        for tag in tags: #iterating across all the tags within the resource
            if tag['Key']=='Name': #checking if there is a tag called 'Name' (in your case replace with 'Owner') and if yes set the flag to 1.
                flag=1
        if flag==0: #if the flag is 0 for the resource it indicates that the tag with key 'Name' is not there. Then, print that specific resource.
            print(resource)
