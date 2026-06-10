"""
Milestone 4 — Embedding + vector store + retrieval.

  build_index()        embed all chunks (all-MiniLM-L6-v2) -> ChromaDB with metadata
  retrieve(query, k)   semantic search, returns top-k chunks + source + distance

The collection uses cosine distance (hnsw:space = cosine), so distances run 0..2 where
lower is more similar — a good match is well under ~0.5, matching the assignment's scale.

Run `python embed.py` to (re)build the index and test retrieval on 3 eval questions.
"""

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import build_chunks

MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DIR = str(Path(__file__).parent / "chroma_db")
COLLECTION = "unifi_guide"

_model = None


def get_model():
    """Lazy-load the embedding model once (downloads ~80 MB on first run)."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def get_client():
    return chromadb.PersistentClient(path=CHROMA_DIR)


def build_index():
    """Embed every chunk and (re)load it into ChromaDB with source metadata."""
    chunks = build_chunks()
    client = get_client()

    # Rebuild from scratch so re-runs are idempotent.
    if COLLECTION in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION)
    collection = client.create_collection(
        name=COLLECTION, metadata={"hnsw:space": "cosine"}
    )

    embeddings = get_model().encode(
        [c["text"] for c in chunks], show_progress_bar=True, batch_size=64
    )

    collection.add(
        ids=[c["id"] for c in chunks],
        embeddings=[e.tolist() for e in embeddings],
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
    )
    print(f"Indexed {collection.count()} chunks into '{COLLECTION}' ({CHROMA_DIR})")
    return collection


def retrieve(query, k=5):
    """Return the top-k chunks for a query: [{text, source, chunk_index, distance}, ...]."""
    collection = get_client().get_collection(COLLECTION)
    q_emb = get_model().encode([query])
    res = collection.query(query_embeddings=[q_emb[0].tolist()], n_results=k)
    return [
        {
            "text": doc,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": dist,
        }
        for doc, meta, dist in zip(
            res["documents"][0], res["metadatas"][0], res["distances"][0]
        )
    ]


# Three of the five evaluation questions (gateway / PoE / VLAN coverage).
TEST_QUERIES = [
    "Does the UniFi Cloud Gateway Ultra have a built-in Wi-Fi access point?",
    "What PoE standard does a U7 Pro access point need to be powered?",
    "Why do people recommend putting IoT / smart-home devices on a separate VLAN?",
]


def main():
    build_index()
    for q in TEST_QUERIES:
        print("\n" + "=" * 78)
        print(f"QUERY: {q}")
        print("=" * 78)
        for i, r in enumerate(retrieve(q, k=5), 1):
            snippet = " ".join(r["text"].split())[:240]
            print(f"\n{i}. distance={r['distance']:.3f}  source={r['source']} "
                  f"(chunk {r['chunk_index']})")
            print(f"   {snippet}...")


if __name__ == "__main__":
    main()
