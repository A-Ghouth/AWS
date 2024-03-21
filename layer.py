from zipfile import ZipFile
import boto3
import os
import shutil
pkg = 'requests'  


s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')


if os.path.exists('python'):
    shutil.rmtree('python')

os.makedirs('python')


os.system(f'pip3 install {pkg} -t python')

zip_file = f'{pkg}.zip'
os.system(f'zip -r {zip_file} python')

file_path = f'layers/{zip_file}'
s3_client.upload_file(zip_file, 'creating.bucket.demo', file_path)

lambda_client.publish_layer_version(
    LayerName= pkg,
    Content={
        'S3Bucket': 'creating.bucket.demo',
        'S3Key': file_path,

    },
    CompatibleRuntimes=[
        'python3.10',
    ],
)
