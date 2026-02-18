Real-Time YouTube Video Question Answering System using RAG


Architecture - ![Model Architecture](<RAG Pipeline.png>)

Demo Video - ![demo video](<Screenshot 2026-02-18 183655.png>)


TubeTalk - steps

1. working RAG - Pipeline
   indexing pipeline -> Loading - Splitting - Embedding - vector store 
   query pipeline -> Retrieval - Augmentation - Generation

2. UI impelementation done 

3. implement backend api - done 

process video transcript - process query 
process indexing step on video transcript api
run rag query pipeline on query api

3. improvements in RAG
    scalability - namespace indexing in pinecone
        notes : named spaces might be cleaned periodically to save database space (otherwise it leads to much databse )

        each unique video id embedding is stored and now many users can query to the same namespace , no need of pre-processing

        saves - embedding cost, quick response, prevent re-indexing 


----- next level improvement

1. model evaluation (LangSmith)
2. memory based RAG (LangGraph)
3. rate limiter (slowapi)
4. model deployment (Render/AWS)