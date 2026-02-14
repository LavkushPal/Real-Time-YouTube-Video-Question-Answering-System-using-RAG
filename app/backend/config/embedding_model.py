import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from dotenv import find_dotenv,load_dotenv

load_dotenv(find_dotenv())

api_key = os.getenv('GEMINI_API_KEY')

gemini_model = GoogleGenerativeAIEmbeddings(
    api_key=api_key,
    model='models/gemini-embedding-001'
)

chat_model=ChatGoogleGenerativeAI(
    api_key=api_key,
    model="models/gemini-3-pro-preview",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
)




