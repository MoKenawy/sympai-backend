import boto3

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('INIT_PATHS_DIR'))


# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

USER_TABLE_NAME = os.getenv('USER_TABLE_NAME')

# Define table creation with username as the primary key and SessionId as the sort key
table = dynamodb.create_table(
    TableName=USER_TABLE_NAME,
    KeySchema=[
        {"AttributeName": "username", "KeyType": "HASH"},  # Partition key
        {"AttributeName": "email", "KeyType": "RANGE"}  # Sort key
    ],
    AttributeDefinitions=[
        {"AttributeName": "username", "AttributeType": "S"},
        {"AttributeName": "email", "AttributeType": "S"}
    ],
    BillingMode="PAY_PER_REQUEST"
)

# Wait until the table is created
table.meta.client.get_waiter('table_exists').wait(TableName='UserTable')

print("Table status:", table.table_status)
