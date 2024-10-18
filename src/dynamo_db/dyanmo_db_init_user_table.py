import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Define table creation with username as the primary key and SessionId as the sort key
table = dynamodb.create_table(
    TableName='UserTable',
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
