from langchain_text_splitters import RecursiveCharacterTextSplitter
from huggingface_hub import InferenceClient
from app.core.config import settings
from app.core.database import get_connection, release_connection
from app.utils.document_loader import load_all_documents, LoadedDocument
from app.utils.text_normalizer import clean_raw_text
from app.utils.semantic_splitter import split_by_semantic_type
from dataclasses import dataclass
from typing import Optional
import json
import os

CHUNK_SIZE = 900
CHUNK_OVERLAP = 200
DOCS_FOLDER = "data/documents"

@dataclass
class Chunk:
    content: str
    source: str
    type: str
    page: Optional[int] = None

def get_embeddings(text: str) -> list[float]:
    client = InferenceClient(token=settings.HF_TOKEN)
    result = client.feature_extraction(text, model=settings.EMBEDDING_MODEL)
    if isinstance(result[0], list):
        return result[0]
    return list(result)

def split_into_chunks(docs: list[LoadedDocument]) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )

    chunks: list[Chunk] = []

    for doc in docs:
        # Normalize dulu
        cleaned = clean_raw_text(doc.content)

        # Kalau txt, pakai semantic splitter dulu
        if doc.type == "txt":
            semantic_blocks = split_by_semantic_type(cleaned)
            for block in semantic_blocks:
                sub_chunks = splitter.split_text(block.content)
                for c in sub_chunks:
                    chunks.append(Chunk(
                        content=c,
                        source=doc.source,
                        type=block.type,
                        page=doc.page
                    ))
        else:
            sub_chunks = splitter.split_text(cleaned)
            for c in sub_chunks:
                chunks.append(Chunk(
                    content=c,
                    source=doc.source,
                    type=doc.type,
                    page=doc.page
                ))

    print(f"Created {len(chunks)} chunks")
    return chunks

def insert_chunks_to_db(chunks: list[Chunk]) -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            print("Clearing old data...")
            cur.execute("DELETE FROM rag_chunks")

            print(f"Inserting {len(chunks)} chunks...")
            for i, chunk in enumerate(chunks):
                embedding = get_embeddings(chunk.content)
                metadata = {
                    "source": chunk.source,
                    "type": chunk.type,
                    "page": chunk.page,
                }
                cur.execute(
                    "INSERT INTO rag_chunks (content, metadata, embedding) VALUES (%s, %s, %s)",
                    (chunk.content, json.dumps(metadata), f"[{','.join(map(str, embedding))}]")
                )
                if (i + 1) % 5 == 0 or i == len(chunks) - 1:
                    print(f"Progress: {i + 1}/{len(chunks)}")

            conn.commit()
            cur.execute("SELECT COUNT(*) FROM rag_chunks")
            count = cur.fetchone()[0]
            print(f"\nTotal chunks in database: {count}")
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        release_connection(conn)

def run_ingestion(docs_folder: str = DOCS_FOLDER) -> dict:
    print("Starting document processing...\n")

    docs = load_all_documents(docs_folder)
    if not docs:
        return {"status": "error", "message": "No documents found"}

    chunks = split_into_chunks(docs)
    insert_chunks_to_db(chunks)

    return {"status": "success", "chunks_inserted": len(chunks)}
