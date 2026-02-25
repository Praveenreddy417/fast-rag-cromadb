from openai import OpenAI
from app.services.vector_store import get_retriever

client = OpenAI()

def generate_answer(question: str) -> str:
    retriever = get_retriever()

    results = retriever.query(
        query_texts=[question],
        n_results=3
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "The information is not available in the provided documents."

    context = "\n\n".join(documents)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """You are a strict document-based assistant.
Answer ONLY from the context.
If answer not in context, say:
'The information is not available in the provided documents.'
"""
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ]
    )

    print("Documents retrieved:", response.choices[0].message.content)  # DEBUG
    return response.choices[0].message.content
