from schemas.schema import AWSConfig
from utils.aws_session import get_aws_session

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('INIT_PATHS_DIR'))

import init  # noqa: E402, F401

# Load environment variables from .env file
load_dotenv()

# Load AWS credentials from environment variables
aws_access_key_id = str(os.getenv('AWS_ACCESS_KEY_ID'))
aws_secret_access_key = str(os.getenv('AWS_SECRET_ACCESS_KEY'))
aws_region=str(os.environ.get("AWS_REGION"))


aws_config = AWSConfig(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_region=aws_region)
aws_session = get_aws_session(aws_config)




# Dynamo DB init
## Dynamo DB table name
CHAT_HISTORY_TABLE_NAME = "SessionTable"
