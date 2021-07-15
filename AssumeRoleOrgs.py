import boto3
import json
import sys

#Initialize clients
org=boto3.client('organizations')
sts=boto3.client('sts')

#Access Key to find
key_id_to_find='AKIAXYZABC123' #replace the access key here

#Iterate over accounts by paginating
paginator = org.get_paginator('list_accounts')
pages= paginator.paginate()
for page in pages:
    account=page['Accounts']
    for acc in account:
        #checking only 'Created' accounts and not 'Invited' ones
        if acc['JoinedMethod']=='CREATED':
            role_arn='arn:aws:iam::'+acc['Id']+':role/OrganizationAccountAccessRole' #Role ARN of OrganizationAccountAccessRole
            role=sts.assume_role(RoleArn=role_arn,RoleSessionName='Test')
            iam=boto3.client('iam',aws_access_key_id=role["Credentials"]["AccessKeyId"],aws_secret_access_key=role["Credentials"]["SecretAccessKey"],aws_session_token=role["Credentials"]["SessionToken"]) #Setting credentials of Assumed Role
            #Listing out IAM users and paginating the users
            iam_paginator=iam.get_paginator('list_users')
            iam_pages=iam_paginator.paginate()
            for iam_page in iam_pages:
                users=iam_page['Users']
                #iterating over the users
                for user in users:
                    #list out access keys of the user
                    access_keys=iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
                    for iter in access_keys:
                        #compare access keys of user to that of the access key to find
                        if iter['AccessKeyId']==key_id_to_find:
                            print("Access key found in user ",user['Arn']) #access key found
                            sys.exit() #exit from script execution since it is found
                        else:
                            continue
            print("Access Key not found")
        else:
            continue
