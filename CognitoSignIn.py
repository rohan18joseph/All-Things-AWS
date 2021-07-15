import json
import boto3

client=boto3.client('cognito-idp')
response = client.initiate_auth(
        ClientMetadata={
                'UserPoolId': 'us-east-1_xxxxxxx'
            },
        ClientId='xxxxxxxxxx',
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': 'xxxxxx@xxxxx.com',
            'PASSWORD': 'xxxxxxxxxxxxx'
        }
    )
print(response)
