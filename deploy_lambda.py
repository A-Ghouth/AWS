import boto3
import os
import time

func_name = 'main-function'
s3_bucket = "creating.bucket.demo"
user_id = ' '
location = 'ap-northeast-2'

# For Attaching Layers to the Function
pkgs = [
    {'name' : 'requests', 'version' : 2},
    {'name' : 'mysql', 'version' : 1},
    {'name' : 'mysql_connector', 'version' : 1},
    {'name' : 'boto3', 'version' : 1}
    ]

## 1. Upload Lambda_Function.py to S3 ---------------------------------------------------------------
os.system(f'zip {func_name}.zip lambda_function.py')

s3 = boto3.client('s3')
s3.upload_file(f'{func_name}.zip', s3_bucket, f'lambda_functions/{func_name}.zip')

## 2.Create a Lambda Function -----------------------------------------------------------------------
client = boto3.client('lambda')

response = client.create_function(
    FunctionName= func_name,
    Runtime='python3.10',
    Handler='lambda_function.lambda_handler',
    Code={
        'S3Bucket': s3_bucket,
        'S3Key': f'lambda_functions/{func_name}.zip'
    },
    Role=f'arn:aws:iam::{user_id}:role/AWSLambda_FullAccess_role' ,
    Layers= [f'arn:aws:lambda:{location}:{user_id}:layer:{pkg["name"]}:{pkg["version"]}' for pkg in pkgs]
)

client.add_permission(
    FunctionName= func_name,
    StatementId='s3-access',
    Action='lambda:InvokeFunction',
    Principal='s3.amazonaws.com'
)

## 3.Add an S3 trigger to the function -----------------------------------------------------------------------
time.sleep(5)
s3_client = boto3.client('s3')

trigger_configuration = {
    'Id': 'lambda_functions_trigger',
    'LambdaFunctionArn': f'arn:aws:lambda:{location}:{user_id}:function:{func_name}',
    'Events': ['s3:ObjectCreated:*'],
    'Filter': {'Key': {'FilterRules': [{'Name': 'prefix', 'Value': 'lambda_functions/'}]}}
}

# Create the S3 notification trigger
s3_client.put_bucket_notification_configuration(
    Bucket= s3_bucket,
    NotificationConfiguration={
        'LambdaFunctionConfigurations': [trigger_configuration]
    }
)