import json
import boto3 

#Initialize Clients
cognito = boto3.client('cognito-identity')

#note:Please ensure that your credentials are configured and make sure to replace values in <> with appropriate values.

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
#Generating credentials
credentials = cognito.get_credentials_for_identity(
    IdentityId=identity['IdentityId'],
    Logins={'cognito-identity.amazonaws.com':identity['Token']}
)
#Displaying the generated credentials
print("Access Key ID: ",credentials['Credentials']['AccessKeyId'])
print("Secret Access Key: ",credentials['Credentials']['SecretKey'])
print("Session Token: ",credentials['Credentials']['SessionToken'])
