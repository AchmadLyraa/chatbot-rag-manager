import re

def clean_raw_text(raw: str) -> str:
    # Samain line ending
    text = raw.replace("\r\n", "\n")
    # Hapus spasi awal & akhir tiap baris
    text = "\n".join(line.strip() for line in text.split("\n"))
    # Ganti lebih dari 2 newline jadi maksimal 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Hapus trailing whitespace tiap baris
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    # Hapus spasi berlebihan
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()
