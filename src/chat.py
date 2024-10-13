
from config import CHAT_HISTORY_TABLE_NAME, aws_session
from dynamo_db.message_history import get_chat_hist
from models.biomistral import llm
from schemas.schema import GetChatHistProps, InferenceSchema

def chatbot_with_DynamoDB(inference_config: InferenceSchema):

    # sys_msg = (SystemMessage(content=SYSTEM_PROMPT))
    # chat_history.append(sys_msg)

    greeting_msg = "Hello , How can i help you"
    print(greeting_msg)
    model = inference_config.model
    chat_history = inference_config.chat_history

    while True:
        user_input = input()
        print(f"User: {user_input}")

        if user_input == "exit":
            break

        chat_history.add_user_message(user_input)
        # print(F"DEBUG >> {chat_history.messages}")
        response = model.invoke(chat_history.messages)
        # print(f"DEBUG >> Response: {response}")
        ai_msg = response.content
        print(f"SymptomSense: {ai_msg}")
        chat_history.add_ai_message(ai_msg)
    # Chat History
    print(chat_history)


if __name__ == "__main__":
    chat_hist_props = GetChatHistProps(
        table_name= CHAT_HISTORY_TABLE_NAME,
        session_id= "1",
        boto3_session=aws_session
    )
    # continue_chat_chain.invoke(chat_hist_props)
    hist = get_chat_hist(chat_hist_props)
    inference_config = InferenceSchema(
        model=llm,
        chat_history=hist
    )
