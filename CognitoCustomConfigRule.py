import json
import boto3

cognito = boto3.client('cognito-idp')
config = boto3.client('config')

def lambda_handler(event,context):
    
    userpools = cognito.list_user_pools(MaxResults=60) #listing user pools
    userpool_list = userpools['UserPools']
    userpool_ids = []
    
    for i in userpool_list:
        userpool_ids.append(i['Id']) #fetching userpool IDs
    
    evaluations = [] #list that will contain the evaluations
    orderingtime = json.loads(event['invokingEvent'])['notificationCreationTime']
    for pool in userpool_ids:
        userpool_describe = cognito.describe_user_pool(
                UserPoolId = pool
            )['UserPool'] #describing the user pool
        if 'UserPoolAddOns' in userpool_describe: #Checking if Advacned security has either been set as Yes, No, or Audit
            if userpool_describe['UserPoolAddOns']['AdvancedSecurityMode']!='OFF': #Checking if Advanced Security is either enforced or in audit
                 evaluations.append(
                    {
                    'ComplianceResourceType': 'AWS::::Account',
                    'ComplianceResourceId': pool,
                    'ComplianceType': 'COMPLIANT',
                    'Annotation': 'Advanced Security is either in Audit or Enforced.',
                    'OrderingTimestamp': orderingtime
                    }
                ) #Adding evaluation item as Compliant
            else:
                evaluations.append(
                    {
                    'ComplianceResourceType': 'AWS::::Account',
                    'ComplianceResourceId': pool,
                    'ComplianceType': 'NON_COMPLIANT',
                    'Annotation': 'Advanced Security is set to OFF',
                    'OrderingTimestamp': orderingtime
                    }
                ) #Adding evaluation item as non Compliant
        else:
             evaluations.append(
                    {
                    'ComplianceResourceType': 'AWS::::Account',
                    'ComplianceResourceId': pool,
                    'ComplianceType': 'NON_COMPLIANT',
                    'Annotation': 'Advanced Security is not enabled.',
                    'OrderingTimestamp': orderingtime
                    }
                ) #Adding evaluation item as Non-compliant
    result_token = event['resultToken']
    response = config.put_evaluations(
                          Evaluations = evaluations,
                            ResultToken = result_token,
                            TestMode = False
                        ) #Sending evaluation items to Config
