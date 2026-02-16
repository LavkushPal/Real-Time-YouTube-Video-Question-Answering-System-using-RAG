from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .controllers.vector_store import store_embedding
from dotenv import load_dotenv

load_dotenv()

def process_transcript(yt_link:str):
    try:
        # Load YouTube video transcript in chunks of 30 seconds without video info
        
        # loader = YoutubeLoader.from_youtube_url(
        #     "https://www.youtube.com/watch?v=LpHfmr1CKEI&list=PL4alkdQ6KryiM3jkLe87g8o6zZgwADP60&index=2",
        #     add_video_info=False,
        #     transcript_format=TranscriptFormat.CHUNKS,
        #     chunk_size_seconds=30
        # )

        loader = YoutubeLoader.from_youtube_url(
            yt_link,
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

        store_embedding(chunks)

        print("done")

        
    except Exception as e:
        print(f"Error: {e}")