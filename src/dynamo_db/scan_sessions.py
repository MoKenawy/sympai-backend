import boto3

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('INIT_PATHS_DIR'))

import init  # noqa: E402, F401
from config import aws_config , CHAT_HISTORY_TABLE_NAME


# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb',
                            region_name = aws_config.aws_region,
                          aws_access_key_id = aws_config.aws_access_key_id,
                          aws_secret_access_key = aws_config.aws_secret_access_key)

print(f"got dynamodb session: {dynamodb}") 
# Select your DynamoDB table
table_name = CHAT_HISTORY_TABLE_NAME # Replace with your table name
table = dynamodb.Table(table_name)



# Scan the table to get all SessionId(s) (partition key)
def get_all_session_ids():
    session_ids = []
    response = table.scan(ProjectionExpression='SessionId')  # Use the partition key name
    
    # Collect all SessionIds from the response
    session_ids.extend(item['SessionId'] for item in response['Items'])
    
    # Handle pagination (if there's more data)
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression='SessionId',
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        session_ids.extend(item['SessionId'] for item in response['Items'])
    
    return session_ids
