from pinecone import Pinecone,Metric
from langchain_pinecone import PineconeVectorStore
import os
from dotenv import load_dotenv, find_dotenv


# Load .env (searches upward from this file)
load_dotenv(find_dotenv())

api_key = os.getenv('PINECONE_API_KEY')

if not api_key:
    raise RuntimeError('PINECONE_API_KEY environment variable not set')

pc_db = Pinecone(api_key=api_key)
