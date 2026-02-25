import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from ingest import CHROMA_PATH

def get_retriever():
    CHROMA_PATH = "app/db/chroma_db"
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )

    client = chromadb.PersistentClient(
    path=CHROMA_PATH
   )

    collection = client.get_collection(
        name="my_collection",
        embedding_function=openai_ef
    )

    print("Collection count:", collection.count())  # DEBUG

    return collection



