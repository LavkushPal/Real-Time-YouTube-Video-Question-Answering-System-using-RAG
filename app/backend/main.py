from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from langchain_pinecone import PineconeVectorStore

from app.backend.controllers.vector_store import embedding_retriever,store_embedding
from dotenv import load_dotenv

load_dotenv()


try:
    # Load YouTube video transcript in chunks of 30 seconds without video info
    
    loader = YoutubeLoader.from_youtube_url(
        "https://www.youtube.com/watch?v=LpHfmr1CKEI&list=PL4alkdQ6KryiM3jkLe87g8o6zZgwADP60&index=2",
        add_video_info=False,
        transcript_format=TranscriptFormat.CHUNKS,
        chunk_size_seconds=30
    )

    docs=loader.load()

    full_transcript = " "
    for doc in docs: 
        full_transcript += doc.page_content


    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks=splitter.create_documents([full_transcript])

    # print(chunks[4])
    # print(full_transcript) 

    store_embedding(chunks)
    retriever=embedding_retriever()

    docs = retriever.invoke('what we are doing in this video and project')

    print(docs)



except Exception as e:
    print(f"Error: {e}")