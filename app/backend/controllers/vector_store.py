from app.backend.models.pinecone_index import vector_store



def store_embedding(docs):
    try:
        vector_store.add_documents(documents=docs)
    
    except Exception as e:
        print(f"embedding stores failed {e}")


def embedding_retriever():
    try:
        retriever =vector_store.as_retriever(
            search_type='similarity',
            search_kwargs={'k':3,'lambda_mult':0.5}
        )

        return retriever

    except Exception as e:
        print(f"embedding retrieval failed {e}")

