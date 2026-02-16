from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .Indexing_pipeline import process_transcript
from .controllers.vector_store import clean_index
from .query_pipeline import process_query

app = FastAPI()


class TranscriptRequest(BaseModel):
    activeUrl:str

class QueryRequest(BaseModel):
    query:str

    

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
def read_root():
    return {"message": "server is running"}


@app.post('/api/process-transcript')
def indexing(data:TranscriptRequest):
    # print('url:',data.activeUrl)

    clean_index() #clean index before processing next video

    process_transcript(data.activeUrl)

    return {
        "recieved url":data.activeUrl,
        "processing":'done'
    }


@app.post('/api/process-query')
def processing(data:QueryRequest):
      
    response=process_query(data.query)

    return {
        "output": response
    } 
      