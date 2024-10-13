from langchain.schema.runnable import RunnableLambda

from config import CHAT_HISTORY_TABLE_NAME, aws_session
from dynamo_db.message_history import get_chat_hist
from chat import chatbot_with_DynamoDB
from models.biomistral import llm as biomistral
# User Inference for Context history
from langchain_community.chat_message_histories import (
    DynamoDBChatMessageHistory,
)

import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('INIT_PATHS_DIR'))

from schemas.schema import ChatProps, GetChatHistProps , UserInferenceInput  # noqa: E402
from schemas.schema import UserInferenceInput  # noqa: E402, F811
from langchain_core.messages import SystemMessage, trim_messages




# Chains

get_chat_hist_invoke = RunnableLambda(lambda x: get_chat_hist(x))
converse = RunnableLambda(chatbot_with_DynamoDB)

chat = RunnableLambda(lambda x : biomistral.invoke(x.messages))



def user_inference(input: UserInferenceInput) -> DynamoDBChatMessageHistory:
    input.chat_history.add_user_message(input.prompt)
    return input.chat_history

# Chat with history
history_preprocess = RunnableLambda(lambda x : x.messages)
user_inference_invoke = RunnableLambda(user_inference)

response_processing = RunnableLambda(lambda x : print(x.content))

update_db = RunnableLambda(lambda x : print(x.content))

chat_with_history_chain =  user_inference_invoke | history_preprocess | biomistral | response_processing


# New chat

def add_user_message_to_history(chatProps: ChatProps) -> ChatProps:
    chatProps.chat_history.add_user_message(chatProps.prompt)
    return chatProps



trimmer = trim_messages(
    max_tokens=4096,
    strategy="last",
    token_counter=biomistral,
    include_system=True,
    allow_partial=False,
    start_on="human",
)


def trim_history(chatProps: ChatProps) -> ChatProps:
    chatProps.trimmed_chat_history = trimmer.invoke(chatProps.chat_history.messages)
    return chatProps

# New chat Chain
def prompt_LLM_with_history(chatProps: ChatProps):
    response = biomistral.invoke(chatProps.trimmed_chat_history)
    chatProps.response = response.content
    return chatProps

def add_ai_message_to_history(chatProps: ChatProps):
    chatProps.chat_history.add_ai_message(chatProps.response)
    return chatProps

def chatUI(chatProps: ChatProps):
    print(f"response : {chatProps.response}")
    return chatProps


add_user_message_to_history_invoke = RunnableLambda(add_user_message_to_history)
trim_history_invoke = RunnableLambda(trim_history)
prompt_LLM_with_history_invoke = RunnableLambda(prompt_LLM_with_history)
add_ai_message_to_history_invoke = RunnableLambda(add_ai_message_to_history)
chatUI_invoke = RunnableLambda(chatUI)



new_chat_chain = add_user_message_to_history_invoke | trim_history_invoke | prompt_LLM_with_history_invoke | add_ai_message_to_history_invoke | chatUI_invoke


if __name__ == "__main__":
    chat_hist_props = GetChatHistProps(
        table_name= CHAT_HISTORY_TABLE_NAME,
        session_id= "1",
        boto3_session = aws_session
    )

    # continue_chat_chain.invoke(chat_hist_props)
    # hist = get_chat_hist_invoke.invoke(chat_hist_props)
    # print(hist.messages)
    # response = chat.invoke(hist)
    # print(response.content)

    chat_history = get_chat_hist(chat_hist_props)
    print(f"Chat History : {chat_history.messages}")

    chat_props = ChatProps(
        chat_history = chat_history,
        prompt= "It's intermittent'",
    )
    chat_props = new_chat_chain.invoke(chat_props)

    # user_inference_props = UserInferenceInput(
    #     chat_history = get_chat_hist(chat_hist_props),
    #     prompt = "my name is mohammed"
    # )

    # chat_with_history_chain.invoke(user_inference_props)








