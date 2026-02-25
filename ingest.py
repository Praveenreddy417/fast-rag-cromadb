import os
import chromadb
from dotenv import load_dotenv
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from app.services.pdf_loader import load_pdfs_from_directory

CHROMA_PATH = "app/db/chroma_db"
PDF_PATH = "data"

load_dotenv()
def ingest_documents():
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )

    client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


    collection = client.get_or_create_collection(
        name="my_collection",
        embedding_function=openai_ef
    )

    # Load text
    text = load_pdfs_from_directory(PDF_PATH)

    if not text:
        print("No text extracted from PDFs.")
        return

    # Simple chunking
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]

    ids = [f"id_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        ids=ids
    )

    print("Ingestion complete.")
    print("Total stored:", collection.count())


if __name__ == "__main__":
    ingest_documents()
