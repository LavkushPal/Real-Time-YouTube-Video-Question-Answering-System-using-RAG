from ..models.pinecone_index import vector_store


def store_embedding(docs,video_id):
    try:
        vector_store.add_documents(documents=docs, namespace=video_id)
    
    except Exception as e:
        print(f"embedding stores failed {e}")

def clean_index():
    try:
        index = vector_store._index   # underlying pinecone index
        index.delete(delete_all=True)
        print("Index cleaned successfully")

    except Exception as e:
        print(f"Index cleanup failed: {e}")

def embedding_retriever(video_id):
    try:
        retriever =vector_store.as_retriever(
            search_type='similarity',
            search_kwargs={
                'k':3,
                'lambda_mult':0.5,
                "namespace": video_id
            }
        )

        return retriever

    except Exception as e:
        print(f"embedding retrieval failed {e}")



def embedding_exists(video_id: str) -> bool:
    try:
        index = vector_store._index
        
        # Describe index stats
        stats = index.describe_index_stats()

        # Check if namespace exists and has vectors
        if video_id in stats.get("namespaces", {}):
            vector_count = stats["namespaces"][video_id]["vector_count"]
            return vector_count > 0
        
        return False

    except Exception as e:
        print(f"Failed to check embedding existence: {e}")
        return False
