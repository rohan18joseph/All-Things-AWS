import boto3 
import json

#initializing Cognito client
cognito=boto3.client('cognito-idp')

#Add your userpool ID here
userpool_id='INSERT_USERPOOL_ID'

# Making the list-users call
resp = cognito.list_users(UserPoolId=userpool_id)['Users']
#Adding all usernames to a single list named usernames
usernames=[user['Username'] for user in resp]
#Iterating across all the usernames and list out the auth events of the user
for uname in usernames:
    response = cognito.admin_list_user_auth_events(
        UserPoolId=userpool_id,
        Username=uname
    )
    events=response['AuthEvents']
    #Iterating across all auth events for the user
    for auth_event in events:
        try:
            #print(auth_event)
            event_id = auth_event['EventId']
            #Naming object in the format '<username>___EventID__<eventID>.json'
            object_name = uname+"___EventId__"+event_id+".json"
            finding = json.dumps(auth_event, indent=4, default=str)
            upload_to_bucket(object_s3=finding,key_s3=object_name) #function to upload finding into S3
        except Exception as error:
            print (error)


def upload_to_bucket(object_s3,key_s3):
    try:
        clientS3 = boto3.client('s3')
        #Enter your S3 bucket name here. 
        bucket_name="INSERT_S3_BUCKETNAME"
        #Adding object into S3 bucket bucket_name
        response = clientS3.put_object(
            Body=object_s3,
            Bucket=bucket_name,
            ContentEncoding='json',
            Key=key_s3,)
    except Exception as error:
        print (error)
