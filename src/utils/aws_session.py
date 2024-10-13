
from schemas.schema import AWSConfig
import boto3
from botocore.session import get_session
from boto3.session import Session

def get_aws_session(aws_config : AWSConfig):
    custom_botocore_session = get_session()

    # Step 2: Use your custom Session class to create a session
    custom_session = Session(
        aws_access_key_id = aws_config.aws_access_key_id,
        aws_secret_access_key = aws_config.aws_secret_access_key,
        region_name = aws_config.aws_region,
        botocore_session=custom_botocore_session
    )

    # Step 3: Pass this custom session into boto3
    boto3_session = boto3.Session(botocore_session=custom_session._session)

    return boto3_session


