from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat

from langchain_text_splitters import RecursiveCharacterTextSplitter

from urllib.parse import urlparse, parse_qs

from .controllers.vector_store import store_embedding,embedding_exists
from dotenv import load_dotenv

load_dotenv()

def extract_video_id(url: str) -> str | None:
    """
    Extracts YouTube video ID from various YouTube URL formats.
    Returns None if no valid ID found.
    """
    parsed_url = urlparse(url)

    # Case 1: Regular watch URL
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]

    # Case 2: Short URL (youtu.be)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path.lstrip("/")

    return None





def process_transcript(yt_link:str):
    try:
        # Load YouTube video transcript in chunks of 30 seconds without video info
        
        # loader = YoutubeLoader.from_youtube_url(
        #     "https://www.youtube.com/watch?v=LpHfmr1CKEI&list=PL4alkdQ6KryiM3jkLe87g8o6zZgwADP60&index=2",
        #     add_video_info=False,
        #     transcript_format=TranscriptFormat.CHUNKS,
        #     chunk_size_seconds=30
        # )

        video_id = extract_video_id(yt_link)

        if video_id==None : 
            raise(Exception("video id could not get extracted during indexing phase. please try again..."))
        
        if embedding_exists(video_id=video_id) :
            return

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

        store_embedding(chunks,video_id)

        print("done")
        
    except Exception as e:
        print(f"Error: {e}")