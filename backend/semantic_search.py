from backend.endee_client import get_index
from backend.embeddings import Embedder

def semantic_search(query, top_k=5):
    index = get_index()
    embedder = Embedder()

    q_vec = embedder.embed(query)
    results = index.query(vector=q_vec, top_k=top_k)

    processed = []
    for r in results:
        score = r.get("similarity", 0)
        confidence = round(score * 100, 2)

        processed.append({
            "id": r["id"],
            "confidence": confidence,
            "meta": r["meta"]
        })

    return processed
