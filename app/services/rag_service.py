# import openai
# from app.core.config import settings
# from app.services.vector_store import query_documents
# openai.api_key = settings.OPENAI_API_KEY
# # client = OpenAI(api_key=settings.OPENAI_API_KEY)

# def generate_answer(question: str):
#     docs = query_documents(question)
#     context = "\n".join(docs)

#     prompt = f"""
#     Answer only from the context below:

#     {context}

#     Question: {question}
#     """

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response["choices"][0]["message"]["content"]

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content
