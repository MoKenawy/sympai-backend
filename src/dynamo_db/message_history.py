from langchain_community.chat_message_histories import (
    DynamoDBChatMessageHistory,
)
from functools import lru_cache

from schemas.schema import GetChatHistProps


# Function using Pydantic model
@lru_cache(maxsize=None)
def get_chat_hist(chat_hist_props : GetChatHistProps):
    chat_history = DynamoDBChatMessageHistory(
        table_name = chat_hist_props.table_name,
        session_id = chat_hist_props.session_id,
        boto3_session = chat_hist_props.boto3_session
    )
    return chat_history