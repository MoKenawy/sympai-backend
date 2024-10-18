import boto3

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('INIT_PATHS_DIR'))

import init  # noqa: E402, F401


# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb')

# Define table name
USER_CHAT_SESSIONS_TABLE_NAME = os.getenv('USER_CHAT_SESSIONS_TABLE_NAME')

# Create the DynamoDB table
table = dynamodb.create_table(
    TableName=USER_CHAT_SESSIONS_TABLE_NAME,
    KeySchema=[
        {"AttributeName": "username", "KeyType": "HASH"},  # Partition key
        {"AttributeName": "SessionId", "KeyType": "RANGE"}  # Sort key
    ],
    AttributeDefinitions=[
        {"AttributeName": "username", "AttributeType": "S"},
        {"AttributeName": "SessionId", "AttributeType": "S"},
    ],
    BillingMode="PAY_PER_REQUEST",  # Use on-demand pricing
)

# Wait until the table exists
table.wait_until_exists()
print(f"Table {USER_SESSIONS_TABLE_NAME} created successfully.")
