import boto3
from botocore.exceptions import ClientError

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
# table_name = CHAT_HISTORY_TABLE_NAME # Replace with your table name
# table = dynamodb.Table(table_name)



# # Scan the table to get all SessionId(s) (partition key)
# def get_all_session_ids():
#     session_ids = []
#     response = table.scan(ProjectionExpression='SessionId')  # Use the partition key name
    
#     # Collect all SessionIds from the response
#     session_ids.extend(item['SessionId'] for item in response['Items'])
    
#     # Handle pagination (if there's more data)
#     while 'LastEvaluatedKey' in response:
#         response = table.scan(
#             ProjectionExpression='SessionId',
#             ExclusiveStartKey=response['LastEvaluatedKey']
#         )
#         session_ids.extend(item['SessionId'] for item in response['Items'])
    
#     return session_ids



# Define table name
USER_CHAT_SESSIONS_TABLE_NAME = os.getenv('USER_CHAT_SESSIONS_TABLE_NAME')

table = dynamodb.Table(USER_CHAT_SESSIONS_TABLE_NAME)


def get_user_chat_sessions(username: str, session_id: str = None):
    """Query a user by username and optionally by session ID from DynamoDB."""
    try:
        if session_id:
            # Query by username and session ID
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('username').eq(username) &
                                       boto3.dynamodb.conditions.Key('SessionId').eq(session_id)
            )
        else:
            # Query by username only
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('username').eq(username)
            )

        if response.get('Items'):
            return response['Items']  # Return the list of items matching the username (and session ID if provided)
        else:
            return None  # User not found
    except ClientError as e:
        print(f"Error querying user: {e.response['Error']['Message']}")
        return None

def get_all_user_chat_sessions(username: str, session_id: str = None):
    return get_user_chat_sessions(username=username)

# Example usage:
if __name__ == "__main__":
    username_to_query = "kenawy"  # Change this to the username you want to query
    session_id_to_query = "session_123"  # Change this to the session ID you want to query (optional)
    user_data = get_user_chat_sessions(username_to_query, session_id_to_query)

    if user_data:
        print(f"User found: {user_data}")
    else:
        print("User not found")