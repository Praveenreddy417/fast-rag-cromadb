from openai import OpenAI
from app.services.vector_store import get_retriever

client = OpenAI()

def generate_answer(question: str, history: list):

    retriever = get_retriever()

    results = retriever.query(
        query_texts=[question],
        n_results=3
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return None, []

    context = "\n\n".join(documents)

    messages = [
        {
            "role": "system",
            "content": """You are a strict KB-based support assistant.
Answer ONLY from the context.
If answer not in context, say:
'The information is not available in the provided documents.'
"""
        }
    ]

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion:\n{question}"
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=messages
    )

    answer = response.choices[0].message.content

    # Fake confidence for now
    confidence = 0.93 if documents else 0.4

    # Dummy KB refs
    kb_refs = [
        {"id": f"kb-{i}", "title": doc[:50]}
        for i, doc in enumerate(documents)
    ]

    return answer, kb_refs, confidence
