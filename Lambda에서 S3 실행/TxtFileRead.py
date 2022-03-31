import json
import boto3
import botocore


def lambda_handler(event, context):
    bucketName = 'serverlesschoi'
    key = 'test.txt'

    s3 = boto3.client('s3')
    data = s3.get_object(Bucket=bucketName, Key=key)
    fileText = data['Body'].read()

    return json.dumps(fileText.decode('UTF-8'))