
from typing import List
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv('INIT_PATHS_DIR'))

from auth.auth_logic import get_current_active_user  # noqa: E402
import init  # noqa: E402, F401
from dynamo_db.message_history import get_chat_hist  # noqa: E402
from dynamo_db.scan_sessions import get_all_user_chat_sessions  # noqa: E402
from models.biomistral import llm  # noqa: E402
from config import aws_session  # noqa: E402
from chains import new_chat_chain  # noqa: E402
from auth.auth_app import auth_app  # noqa: E402, F401
from schemas.schema import ChatProps , GetChatHistProps  # noqa: E402
from auth.auth_schemes import User  # noqa: E402
from schemas.api import GuestChatInput, GuestChatOutput, UserChatInput, UserChatOutput  # noqa: E402


app = FastAPI()

app.mount('/auth', auth_app)

# Define the allowed origins (you can limit this to your frontend URL in production)
origins = [
    "http://localhost:3000",  # Your Next.js frontend URL
    "http://127.0.0.1:3000",  # Another form of localhost URL
    "*",
    "https://master.d3qfb4jv3hhifa.amplifyapp.com",  
]

# Apply the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be included in the request
    allow_methods=["GET", "POST", "OPTIONS"],  # Explicitly allow OPTIONS method
    allow_headers=["*"],  # Allow all headers
)

@app.post("/api/guest_chat", response_model=GuestChatOutput)
def guest_chat(chat_input: GuestChatInput):
    print(f"Guest prompt : {chat_input.prompt}")
    response = llm.invoke(chat_input.prompt)
    print(f"SymAI response : {response.content}")
    return GuestChatOutput(response=response.content)





@app.get("/api/get_user_history")
def get_user_history(session_id : str, current_user: User = Depends(get_current_active_user)):
    try:
        chat_hist_props = GetChatHistProps(
            username=current_user.username,
            session_id= session_id,
            boto3_session = aws_session
        )
        chat_history = get_chat_hist(chat_hist_props)
        
        return chat_history.messages
    
    except Exception as e:
        print(f"Error : {e}")
        return UserChatOutput(response="An Error Occured. Please try again later.")


@app.get("/api/clear_user_history")
def clear_user_history(session_id : str, current_user: User = Depends(get_current_active_user)):
    try:
        chat_hist_props = GetChatHistProps(
            username=current_user.username,
            session_id= session_id,
            boto3_session = aws_session
        )
        chat_history = get_chat_hist(chat_hist_props)
        chat_history.clear()
        return "History Cleared"
    
    except Exception as e:
        print(f"Error : {e}")
        return UserChatOutput(response="An Error Occured. Please try again later.")
    

@app.get("/api/delete_chat")
def delete_chat(session_id : str, current_user: User = Depends(get_current_active_user)):
    try:
        ...
    
    except Exception as e:
        print(f"Error : {e}")
        return UserChatOutput(response="An Error Occured. Please try again later.")


@app.post("/api/user_chat", response_model=UserChatOutput)
def user_chat(user_chat_input: UserChatInput, current_user: User = Depends(get_current_active_user)):
    
    try:
        chat_hist_props = GetChatHistProps(
            username= current_user.username,
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


@app.get("/api/scan_sessions", response_model=List[dict])
def scan_sessions(current_user: User = Depends(get_current_active_user)):
    try:
        # sessions = get_all_session_ids()
        sessions = get_all_user_chat_sessions(current_user.username)
        return sessions
    except Exception as e:
        print(f"Error : {e}")
        return ['An Error Occured. Please try again later.']


# @app.get("/api/scan_sessions", response_model=List[str])
# def scan_sessions():
#     try:
#         sessions = get_all_session_ids()
#         return sessions
#     except Exception as e:
#         print(f"Error : {e}")
#         return ['An Error Occured. Please try again later.']




@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}