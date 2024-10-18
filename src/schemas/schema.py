from langchain_ollama.chat_models import ChatOllama
from pydantic import BaseModel, ConfigDict, Field
from langchain_community.chat_message_histories.dynamodb import DynamoDBChatMessageHistory
from langchain_core.language_models.chat_models import BaseChatModel
from boto3.session import Session
from typing import List

from langchain_core.messages import (
    BaseMessage)


class AWSConfig(BaseModel):
    aws_access_key_id : str
    aws_secret_access_key : str
    aws_region: str


# Pydantic model with arbitrary types allowed
class GetChatHistProps(BaseModel):
    username: str
    session_id: str
    boto3_session: Session

    def __hash__(self):
        return hash((self.username, self.session_id))

    model_config = ConfigDict(arbitrary_types_allowed=True)


class InferenceSchema(BaseModel):
    model: BaseChatModel
    chat_history: DynamoDBChatMessageHistory = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class UserInferenceInput(BaseModel):
    prompt: str
    chat_history: DynamoDBChatMessageHistory
    model_config = ConfigDict(arbitrary_types_allowed=True)


class ChatProps(BaseModel):
    prompt: str = Field(example="I have a headache", min_length=1, max_length= 4096// 2)
    chat_history: DynamoDBChatMessageHistory
    trimmed_chat_history : List[BaseMessage] = None
    response: str = None
    model : ChatOllama = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

