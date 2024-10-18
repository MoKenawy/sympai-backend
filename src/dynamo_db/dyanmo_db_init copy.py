import boto3
from config import aws_config , CHAT_HISTORY_TABLE_NAME

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('INIT_PATHS_DIR'))

import init  # noqa: E402, F401

# Create the DynamoDB resource
dynamodb = boto3.resource('dynamodb',
                            region_name = aws_config.aws_region,
                          aws_access_key_id = aws_config.aws_access_key_id,
                          aws_secret_access_key = aws_config.aws_secret_access_key)

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName= CHAT_HISTORY_TABLE_NAME,
    KeySchema=[{"AttributeName": "SessionId", "KeyType": "HASH"}],
    AttributeDefinitions=[{"AttributeName": "SessionId", "AttributeType": "S"}],
    BillingMode="PAY_PER_REQUEST",
)

# Wait until the table exists.
table.meta.client.get_waiter("table_exists").wait(TableName= CHAT_HISTORY_TABLE_NAME)

# Print out some data about the table.
print(table.item_count)