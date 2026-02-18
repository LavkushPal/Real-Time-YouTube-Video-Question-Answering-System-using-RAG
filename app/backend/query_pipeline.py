from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel,RunnableLambda,RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from .controllers.vector_store import embedding_retriever
from .config.embedding_model import chat_model

from urllib.parse import urlparse, parse_qs

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



def process_query(query:str,yt_link:str):

    try:
        def format_docs(retrieved_docs):
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
            return context_text
        
        prompt= PromptTemplate(
            template="""
                You are a helpful assistant.
                Answer ONLY from the provided transcript context.
                If the context is insufficient, just say you don't know.

                Context: {context}
                Question: {question}
            """,
            input_variables=['context','question']
        )

        video_id=extract_video_id(yt_link)

        retriever = embedding_retriever(video_id=video_id)
        runnable_formater = RunnableLambda(format_docs)
        parser = StrOutputParser()

        parallele_chain = RunnableParallel({
            'context':  retriever | runnable_formater,
            'question' : RunnablePassthrough()
        })

        main_chain = parallele_chain | prompt | chat_model | parser

        response = main_chain.invoke(query)

        print(f"response of query: {response}")

        return response

    except Exception as e:
        print(f"Error: {e}")


# question='what we are doing in this video and project'
# retrieved_docs = retriever.invoke(question)
# final_prompt=prompt.invoke({'context':context_text,'question':question})
# response=chat_model.invoke(final_prompt)