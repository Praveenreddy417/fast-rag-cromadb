import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

client = chromadb.PersistentClient(path="app/db/chroma_db")

embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="pdf_docs",
    embedding_function=embedding_function
)

def add_documents(chunks):
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[str(i)]
        )

def query_documents(query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    return results["documents"][0]
