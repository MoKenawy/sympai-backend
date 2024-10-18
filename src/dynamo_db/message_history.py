from langchain_community.chat_message_histories import (
    DynamoDBChatMessageHistory,
)
from functools import lru_cache
import os
from dotenv import load_dotenv
load_dotenv()


import sys

load_dotenv()
sys.path.append(os.getenv('INIT_PATHS_DIR'))
import init  # noqa: E402, F401

from config import aws_session
from schemas.schema import GetChatHistProps



USER_CHAT_SESSIONS_TABLE_NAME = os.getenv('USER_CHAT_SESSIONS_TABLE_NAME')
USER_CHAT_SESSIONS_TABLE_PK_NAME = os.getenv('USER_CHAT_SESSIONS_TABLE_PK_NAME')
USER_CHAT_SESSIONS_TABLE_SK_NAME = os.getenv('USER_CHAT_SESSIONS_TABLE_SK_NAME')

# Function using Pydantic model
@lru_cache(maxsize=None)
def get_chat_hist(chat_hist_props : GetChatHistProps):
    chat_history = DynamoDBChatMessageHistory(
        table_name = USER_CHAT_SESSIONS_TABLE_NAME,
        primary_key_name= USER_CHAT_SESSIONS_TABLE_PK_NAME,
        key = {USER_CHAT_SESSIONS_TABLE_PK_NAME: chat_hist_props.username, 
               USER_CHAT_SESSIONS_TABLE_SK_NAME: chat_hist_props.session_id},
        session_id= chat_hist_props.session_id,
        boto3_session = chat_hist_props.boto3_session
    )
    return chat_history



if __name__ == "__main__":
    chat_hist_props = GetChatHistProps(
        username= "moken",
        session_id= "1",
        boto3_session = aws_session
    )
    chat_history = get_chat_hist(chat_hist_props)
    chat_history.add_user_message("Hello")
    print(f"Chat History : {chat_history.messages}")