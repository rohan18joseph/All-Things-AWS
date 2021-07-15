import json
import boto3 

#note:Please ensure that your credentials are configured and make sure to replace values in <> with appropriate values.

#Initialize Clients
cognito = boto3.client('cognito-identity')
sts = boto3.client('sts')

identity_pool_id='<insert_identity_pool_id>'
idpool = cognito.describe_identity_pool(
    IdentityPoolId=identity_pool_id
)
identity = cognito.get_open_id_token_for_developer_identity(
    IdentityPoolId=identity_pool_id,
    Logins={
        idpool['DeveloperProviderName']: '<insert_value_here>'
})
print(identity['IdentityId'])
print("============================")
print(identity['Token'])

#Generates AWS Credentials of the authenticated role
credentials = sts.assume_role_with_web_identity(
    RoleArn='<arn_of_authenticated_role>',
    RoleSessionName='<enter_role_session_name>',
    WebIdentityToken=identity['Token'],
    #ProviderId='string',
    #PolicyArns=[ {'arn': 'string'},],
    #Policy='string',
    DurationSeconds=3600
)
print("Access Key ID: ",credentials['Credentials']['AccessKeyId'])
print("Secret Access Key: ",credentials['Credentials']['SecretAccessKey'])
print("Session Token: ",credentials['Credentials']['SessionToken'])
