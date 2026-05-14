from app.core.database import get_connection, release_connection
from app.services.ingestion_service import get_embeddings
from app.core.config import settings
import json

TOP_K = 5
SIMILARITY_THRESHOLD = 0.8

def retrieve_relevant_docs(query: str) -> list[dict]:
    query_embedding = get_embeddings(query)
    embedding_str = f"[{','.join(map(str, query_embedding))}]"

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT file_id, content, meta_data, embedding <=> %s::vector AS score
                FROM rag_chunks
                ORDER BY score ASC
                LIMIT %s
            """, (embedding_str, settings.TOP_K))

            results = cur.fetchall()

        relevant = []
        for file_id, content, meta_data, score in results:
            if score <= settings.SIMILARITY_THRESHOLD:
                doc = {
                    "file_id": file_id,
                    "content": content,
                    "meta_data": meta_data if isinstance(meta_data, dict) else json.loads(meta_data),
                    "score": round(score, 3)
                }
                relevant.append(doc)

        return relevant
    finally:
        release_connection(conn)

def format_docs_as_context(docs: list[dict]) -> str:
    if not docs:
        return "Tidak ada dokumen relevan yang ditemukan."

    parts = []
    for i, doc in enumerate(docs):
        meta = doc["meta_data"]
        meta_info = " | ".join(filter(None, [
            f"Tipe: {meta.get('type', 'unknown')}",
            f"Source: {meta.get('source', 'unknown')}",
            f"Score: {doc['score']}",
        ]))
        parts.append(f"[Dokumen {i+1}] {meta_info}\n{doc['content']}")

    return "\n\n---\n\n".join(parts)
