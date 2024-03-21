import boto3
import time
import mysql.connector
import json

sql_ip = '3.37.49.138'

## --> 1.Create RDS ---------------------------------------------------------------------------------------------
rds = boto3.client('rds')

if rds.describe_db_instances(DBInstanceIdentifier='my-rds-instance'):
    print('RDS instance already exists')
else:
    response = rds.create_db_instance(
        DBInstanceIdentifier='my-rds-instance',
        AllocatedStorage=20,
        DBInstanceClass='db.t2.micro',
        Engine='mysql',
        MasterUsername=' ',
        MasterUserPassword=' ',
        DBName=' '
    )

while True:
    response = rds.describe_db_instances(
        DBInstanceIdentifier='my-rds-instance'
    )

    if response['DBInstances'][0]['DBInstanceStatus'] == 'available':
        print("The RDS instance is done creating.")
        break
    else:
        print("The RDS instance is still creating.")
        time.sleep(10) 

## --> 2.Connect to SQL --> JOSN ---------------------------------------------------------------------------------------------

connection = mysql.connector.connect(
    host= sql_ip,
    port=3306,
    user=' ',
    password=' ',
    database=' ',
)

cursor = connection.cursor()

# Execute the SQL command to get the top 10 customer ids and their total sales
cursor.execute("""
    SELECT CustomerID, SUM(sales) AS total_sales
    FROM orders
    GROUP BY CustomerID
    ORDER BY total_sales DESC
    LIMIT 10;
""")

results = cursor.fetchall()

cursor.close()
connection.close()

## --> 3.Upload JSON to S3 -------------------------------------------------------------------------------------------
converted_data = [{'id': item[0], 'sales': float(item[1])} for item in results]
json_data = json.dumps(converted_data)

with open('results.json', 'w') as f:
    f.write(converted_data)
    
s3 = boto3.client('s3')
s3.upload_file('results.json', 'creating.bucket.demo', 'input/results.json')

## --> 4.create lambda function  -------------------------------------------------------------------------------------------
## --> deploy_lambda.py