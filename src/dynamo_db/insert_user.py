import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserTable')  # Your DynamoDB table name

def insert_user_to_db(username, full_name, email, hashed_password, disabled):
    try:
        table.put_item(
            Item={
                "username": username,
                "full_name": full_name,
                "email": email,
                "hashed_password": hashed_password,
                "disabled": disabled
            }
        )
        return True
    except ClientError as e:
        print(f"Failed to insert user: {e.response['Error']['Message']}")
        return False
