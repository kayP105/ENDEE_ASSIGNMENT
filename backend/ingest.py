import uuid
from pypdf import PdfReader
from backend.embeddings import Embedder
from backend.endee_client import get_index


# --------- CONFIG ---------
CHUNK_SIZE = 400      # words per chunk
CHUNK_OVERLAP = 50    # overlapping words
# --------------------------


def extract_chunks_from_pdf(path):
    """
    Extracts text from a PDF page by page and returns
    deduplicated, overlapping chunks with page numbers.
    """
    reader = PdfReader(path)
    chunks = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue

        words = text.split()
        i = 0

        while i < len(words):
            chunk_words = words[i:i + CHUNK_SIZE]
            chunk_text = " ".join(chunk_words).strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page_number
                })

            i += CHUNK_SIZE - CHUNK_OVERLAP

    # -------- Deduplication --------
    seen = set()
    unique_chunks = []

    for c in chunks:
        normalized = c["text"].lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            unique_chunks.append(c)

    return unique_chunks


def extract_chunks_from_text(text):
    """
    Chunk plain text files with overlap (no pages).
    """
    words = text.split()
    chunks = []
    i = 0

    while i < len(words):
        chunk_words = words[i:i + CHUNK_SIZE]
        chunk_text = " ".join(chunk_words).strip()

        if chunk_text:
            chunks.append({
                "text": chunk_text,
                "page": None
            })

        i += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def ingest_file(path):
    """
    Ingests a TXT or PDF file into Endee with embeddings
    and rich metadata (source + page number).
    """
    index = get_index()
    embedder = Embedder()

    records = []

    if path.lower().endswith(".pdf"):
        chunks = extract_chunks_from_pdf(path)
    else:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = extract_chunks_from_text(text)

    for chunk in chunks:
        records.append({
            "id": str(uuid.uuid4()),
            "vector": embedder.embed(chunk["text"]),
            "meta": {
                "text": chunk["text"],
                "source": path,
                "page": chunk["page"]
            }
        })

    if records:
        index.upsert(records)
