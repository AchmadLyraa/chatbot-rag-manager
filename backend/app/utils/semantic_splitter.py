import re
from dataclasses import dataclass
from typing import Literal

ChunkType = Literal["structure", "news", "csr"]

@dataclass
class SemanticBlock:
    type: ChunkType
    content: str

def split_by_semantic_type(text: str) -> list[SemanticBlock]:
    blocks: list[SemanticBlock] = []

    # === STRUKTUR ORGANISASI ===
    structure_match = re.search(r"STRUKTUR ORGANISASI[\s\S]*?(?=Berita:)", text, re.IGNORECASE)
    if structure_match:
        blocks.append(SemanticBlock(
            type="structure",
            content=structure_match.group(0).strip()
        ))

    # === SISANYA (NEWS / CSR) ===
    remaining = text.replace(structure_match.group(0), "") if structure_match else text
    paragraphs = [p.strip() for p in remaining.split("\n\n") if len(p.strip()) > 50]

    for p in paragraphs:
        chunk_type: ChunkType = "news"
        if re.search(r"CSR|Tanggung Jawab Sosial|UMKM|Bank Sampah|Lansia|Pesisir", p, re.IGNORECASE):
            chunk_type = "csr"
        blocks.append(SemanticBlock(type=chunk_type, content=p))

    return blocks
