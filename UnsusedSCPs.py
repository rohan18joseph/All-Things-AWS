import json
import boto3

client=boto3.client('organizations')

def lambda_handler(event, context):
    # get the policy ID and iterate over them to see if they are attached to targets
    response = client.list_policies(
        Filter='SERVICE_CONTROL_POLICY'
    )
    empty_pols=[]
    for policy in response['Policies']:
        resp = client.list_targets_for_policy(
        PolicyId=policy['Id']
        )
        if len(resp['Targets'])==0:
            empty_pols.append(policy['Id'])
    print("The following SCPS have no targets:")
    print(empty_pols)
    
   lambda_handler()
