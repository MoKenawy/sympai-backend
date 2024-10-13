
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('INIT_PATHS_DIR'))

import init  # noqa: E402, F401
from dynamo_db.message_history import get_chat_hist  # noqa: E402
from dynamo_db.scan_sessions import get_all_session_ids
from models.biomistral import llm  # noqa: E402
from config import aws_session , CHAT_HISTORY_TABLE_NAME  # noqa: E402
from chains import new_chat_chain  # noqa: E402
from schemas.schema import ChatProps , GetChatHistProps  # noqa: E402
from langchain_community.chat_message_histories import (
    DynamoDBChatMessageHistory,
)


app = FastAPI()

# Define the allowed origins (you can limit this to your frontend URL in production)
origins = [
    "http://localhost:3000",  # Your Next.js frontend URL
    "http://127.0.0.1:3000",  # Another form of localhost URL
    "*"
]

# Apply the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be included in the request
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly allow OPTIONS method
    allow_headers=["*"],  # Allow all headers
)

class GuestChatInput(BaseModel):
    prompt: str = Field(example="I have a headache", min_length=1, max_length= 4096// 2)
    max_tokens: int = Field(default=4096, example=4096, ge=1, le=4096)
    temperature: float = Field(default=None, example=0.4)
    top_p: float = Field(default=None, example=0.5)
    n: int = Field(default=None, example=1)
    presence_penalty: float = Field(default=None, example=0.5)
    frequency_penalty: float = Field(default=None, example=0.5)

class GuestChatOutput(BaseModel):
    response: str = Field(example="Hi. I’m SymptomSense, a medical chatbot designed to help you identify your symptoms and offer recommendations. To get started, can you please describe your symptoms in detail? What kind of headache is it? Is it constant or intermittent? Where is the pain located? And what's the intensity on a scale of 1-10?")


@app.post("/api/guest_chat", response_model=GuestChatOutput)
def guest_chat(chat_input: GuestChatInput):
    print(f"Guest prompt : {chat_input.prompt}")
    response = llm.invoke(chat_input.prompt)
    print(f"SymAI response : {response.content}")
    return GuestChatOutput(response=response.content)

# USER CHAT => With Chat History

class UserChatInput(BaseModel):
    prompt: str = Field(example="I have a headache", min_length=1, max_length= 4096// 2)
    table_name : str = Field(example= CHAT_HISTORY_TABLE_NAME, min_length=1)
    session_id: str = Field(example="1", min_length=1)
class UserChatOutput(BaseModel):
    response: str = Field(example="Hi. I’m SymptomSense, a medical chatbot designed to help you identify your symptoms and offer recommendations. To get started, can you please describe your symptoms in detail? What kind of headache is it? Is it constant or intermittent? Where is the pain located? And what's the intensity on a scale of 1-10?")




@app.get("/api/get_user_history")
def get_user_history(session_id : str):
    try:
        chat_hist_props = GetChatHistProps(
            table_name= CHAT_HISTORY_TABLE_NAME,
            session_id= session_id,
            boto3_session = aws_session
        )
        chat_history = get_chat_hist(chat_hist_props)
        
        return chat_history.messages
    
    except Exception as e:
        print(f"Error : {e}")
        return UserChatOutput(response="An Error Occured. Please try again later.")


@app.get("/api/clear_user_history")
def clear_user_history(session_id : str):
    try:
        chat_hist_props = GetChatHistProps(
            table_name= CHAT_HISTORY_TABLE_NAME,
            session_id= session_id,
            boto3_session = aws_session
        )
        chat_history = get_chat_hist(chat_hist_props)
        chat_history.clear()
        return "History Cleared"
    
    except Exception as e:
        print(f"Error : {e}")
        return UserChatOutput(response="An Error Occured. Please try again later.")

@app.post("/api/user_chat", response_model=UserChatOutput)
def user_chat(user_chat_input: UserChatInput):
    try:
        chat_hist_props = GetChatHistProps(
            table_name= user_chat_input.table_name,
            session_id= user_chat_input.session_id,
            boto3_session = aws_session
        )

        chat_history = get_chat_hist(chat_hist_props)


        chat_props = ChatProps(
            chat_history = chat_history,
            prompt= user_chat_input.prompt,
        )
        chat_props = new_chat_chain.invoke(chat_props)
        print(f"Trimmed Chat History : {chat_props.trimmed_chat_history}")
        return UserChatOutput(response=chat_props.response)
    except Exception as e:
        print(f"Error : {e}")
        return UserChatOutput(response="An Error Occured. Please try again later.")


@app.get("/api/scan_sessions", response_model=List[str])
def scan_sessions():
    try:
        sessions = get_all_session_ids()
        return sessions
    except Exception as e:
        print(f"Error : {e}")
        return ['An Error Occured. Please try again later.']




@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}