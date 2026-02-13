from app.backend.config.db import pc_db
from app.backend.config.embedding_model import gemini_model
from pinecone import Metric
from langchain_pinecone import PineconeVectorStore

try:
    # index = pc_db.create_index(
    #     name='yt-transcript',
    #     dimension=1536,
    #     metric=Metric.COSINE,
    #     spec=ServerlessSpec(
    #         cloud=CloudProvider.AWS,
    #         region=AwsRegion.US_WEST_2
    #     )
    # )

    index = pc_db.Index(
        host='https://tubetalk-jpl436q.svc.aped-4627-b74a.pinecone.io',
        name='tubetalk'
    )

except Exception as e:
    print(f"pinecone index creation failed : {e}")


try:
    vector_store = PineconeVectorStore(
        embedding=gemini_model,
        index=index
    )

except Exception as e:
    print(f"pinecone vector store creation failed : {e}")



