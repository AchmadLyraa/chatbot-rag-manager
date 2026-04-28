import google.generativeai as genai
from app.core.config import settings
from app.services.retrieval_service import retrieve_relevant_docs, format_docs_as_context
from typing import Generator

TEMPLATE = """
Kamu adalah asisten AI untuk PLN Nusantara Power Unit Pembangkitan Kaltim Teluk Kariangau.

Aturan:
- Gunakan hanya informasi yang tersedia di bawah ini.
- Jika jawaban tidak ditemukan, jawab: "Maaf, saya tidak punya informasi tentang itu."
- Dilarang menyebutkan kata seperti: konteks, dokumen, sumber, riwayat chat, atau proses internal.
- Jawab langsung, natural, tanpa kalimat pembuka formal.

{context}

Pertanyaan:
{question}

Jawaban:
"""

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel(settings.GEMINI_MODEL)

def format_chat_history(messages: list[dict]) -> str:
    history = []
    for m in messages[:-1]:
        role = "User" if m["role"] == "user" else "Assistant"
        history.append(f"{role}: {m['content']}")
    return "\n".join(history)

def chat_stream(messages: list[dict]) -> Generator[str, None, None]:
    user_query = messages[-1]["content"]
    chat_history = format_chat_history(messages)

    relevant_docs = retrieve_relevant_docs(user_query)
    context = format_docs_as_context(relevant_docs)

    prompt = TEMPLATE.format(context=context, question=user_query)

    if chat_history:
        prompt = f"Riwayat percakapan:\n{chat_history}\n\n{prompt}"

    response = model.generate_content(prompt, stream=True)

    for chunk in response:
        if chunk.text:
            yield chunk.text
