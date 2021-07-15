import boto3
import json

client = boto3.client('cur')

response = client.put_report_definition(
    ReportDefinition={
        'ReportName': '<insert_name_here>',
        'TimeUnit': 'HOURLY',
        'Format': 'Parquet',
        'Compression': 'Parquet',
        'AdditionalSchemaElements': [
            'RESOURCES'
        ],
        'S3Bucket': '<give_the_s3_bucket_here>', #bucket should have sufficient permission
        'S3Prefix': '<insert_name_here>',
        'S3Region': 'us-east-1',
        'AdditionalArtifacts': [
            'ATHENA'
        ],
        'RefreshClosedReports': True,
        'ReportVersioning': 'OVERWRITE_REPORT'
    }
)
'''
resp = client.describe_report_definitions() #to check if the report was created
print(resp)
'''
