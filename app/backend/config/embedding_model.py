import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from dotenv import find_dotenv,load_dotenv

load_dotenv(find_dotenv())

api_key = os.getenv('GEMINI_API_KEY')

gemini_model = GoogleGenerativeAIEmbeddings(
    api_key=api_key,
    model='models/gemini-embedding-001'
)

