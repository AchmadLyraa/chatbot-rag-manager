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
                SELECT content, metadata, embedding <=> %s::vector AS score
                FROM rag_chunks
                ORDER BY score ASC
                LIMIT %s
            """, (embedding_str, settings.TOP_K))

            results = cur.fetchall()

        relevant = []
        for content, metadata, score in results:
            if score <= settings.SIMILARITY_THRESHOLD:
                doc = {
                    "content": content,
                    "metadata": metadata if isinstance(metadata, dict) else json.loads(metadata),
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
        meta = doc["metadata"]
        meta_info = " | ".join(filter(None, [
            f"Tipe: {meta.get('type', 'unknown')}",
            f"Source: {meta.get('source', 'unknown')}",
            f"Score: {doc['score']}",
        ]))
        parts.append(f"[Dokumen {i+1}] {meta_info}\n{doc['content']}")

    return "\n\n---\n\n".join(parts)
