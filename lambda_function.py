import mysql.connector
import json
import requests
import boto3
from datetime import datetime


def lambda_handler(event, context):
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Get the bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    time = event['Records'][0]['eventTime']
    
    # Parse the timestamp string into a datetime object
    timestamp = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    date = timestamp.strftime('%Y-%m-%d')

    # Download the object from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    file_data = response['Body'].read()
    json_data = file_data.decode('utf-8')

    dic = dict()
    
    # Execute the SQL command to get the top 10 customer ids and their total sales
    connection = mysql.connector.connect(
        host='3.37.49.138',
        port=3306,
        user=' ',
        password=' ',
        database=' ',
    )
    cursor = connection.cursor()

    i = 0
    for row in json.loads(json_data):
        id = row.get('id')
        cursor.execute("SELECT CustomerName FROM customers WHERE CustomerID = %s", (id,))
        name = cursor.fetchall()[0][0]
        
        dic[i] = {
            'id' : id,
            'name' : name,
            'date' : date
        }
        i+=1

    cursor.close()
    connection.close() 
        
    response = requests.post('https://virtserver.swaggerhub.com/wcd_de_lab/top10/1.0.0/add', json=dic)
    response_status_code = response.status_code

    return {
        'statusCode': response_status_code,
        'body': 'File processed successfully'
    }
