from pydantic import BaseModel, Field


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

# USER CHAT => With Chat History

class UserChatInput(BaseModel):
    prompt: str = Field(example="I have a headache", min_length=1, max_length= 4096// 2)
    session_id: str = Field(example="1", min_length=1)
class UserChatOutput(BaseModel):
    response: str = Field(example="Hi. I’m SymptomSense, a medical chatbot designed to help you identify your symptoms and offer recommendations. To get started, can you please describe your symptoms in detail? What kind of headache is it? Is it constant or intermittent? Where is the pain located? And what's the intensity on a scale of 1-10?")
