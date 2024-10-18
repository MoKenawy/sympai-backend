import boto3
from botocore.exceptions import ClientError

# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb')

# Replace 'YourTableName' with the actual table name
CHAT_HISTORY_TABLE_NAME = 'UserTable'  # Change this to your actual table name
table = dynamodb.Table(CHAT_HISTORY_TABLE_NAME)

def get_user_by_username(username: str):
    """Query a user by username from DynamoDB."""
    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('username').eq(username)
        )
        
        if response.get('Items'):
            return response['Items']  # Return the list of items matching the username
        else:
            return None  # User not found
    except ClientError as e:
        print(f"Error querying user by username: {e.response['Error']['Message']}")
        return None

# Example usage:
if __name__ == "__main__":
    username_to_query = "moken"  # Change this to the username you want to query
    user_data = get_user_by_username(username_to_query)
    
    if user_data:
        print(f"User found: {user_data}")
    else:
        print("User not found")
