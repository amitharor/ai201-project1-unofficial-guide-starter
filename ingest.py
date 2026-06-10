"""
Milestone 3 — Document ingestion + chunking pipeline.

Three stages, no third-party dependencies:
  load_documents()  -> read every .txt in documents/
  clean_text()      -> strip forum/blog chrome (vote counts, "Reply", banners, etc.)
  chunk_text()      -> recursive split into ~800-char chunks with ~150-char overlap

build_chunks() ties them together and is what Milestone 4 imports to embed.
Run `python ingest.py` to print corpus stats + 5 sample chunks and write chunks.json.
"""

import glob
import json
import os
import re
import statistics
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "documents"
CHUNKS_OUT = Path(__file__).parent / "chunks.json"

# Chunking parameters (from planning.md). 800 chars ~= 180-200 tokens, safely under
# all-MiniLM-L6-v2's 256 word-piece truncation limit.
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


# --------------------------------------------------------------------------- #
# Stage 1: load
# --------------------------------------------------------------------------- #
def load_documents(docs_dir=DOCS_DIR):
    """Read every .txt file in docs_dir. Returns [{source, raw}, ...]."""
    docs = []
    for path in sorted(glob.glob(str(Path(docs_dir) / "*.txt"))):
        raw = Path(path).read_text(encoding="utf-8", errors="ignore")
        docs.append({"source": os.path.basename(path), "raw": raw})
    return docs


# --------------------------------------------------------------------------- #
# Stage 2: clean
# --------------------------------------------------------------------------- #
_HTML_ENTITIES = {
    "&amp;": "&", "&nbsp;": " ", "&#39;": "'", "&quot;": '"',
    "&lt;": "<", "&gt;": ">", "&rsquo;": "’", "&lsquo;": "‘",
    "&ldquo;": "“", "&rdquo;": "”", "&hellip;": "…",
}

# Lines that are pure forum/blog chrome — matched against the *stripped* line.
_JUNK_LINE_PATTERNS = [
    r"\d+",                                       # standalone vote / reply counts ("0", "12")
    r"Reply",
    r"Newest",
    r"Oldest",
    r"Accepted Response",
    r"Created",
    r"Activity",
    r"Avatar for .*",                             # image alt text
    r"This thread is locked.*",
    r"[\d.,]+\s*[KkMm]?\s+views?",                # "11.96K views"
    r"\d+\s+repl(?:y|ies)",                       # "8 replies"
    r"Need Ubiquiti R&D attention.*",             # @UI-Team banner
    r"@UI-Team",
    r"in your post\.?",
    r"(?:a|an|\d+)\s+(?:year|month|week|day|hour|minute)s?\s+ago",
    r"Last updated .*Comments?",                  # blog byline + comment count
    r"\d+\s+Comments?",
    r"In this article",                           # blog table-of-contents header
    r"If you buy through our links.*",            # affiliate ad
    r"Learn More\.?",
    r".*Avatar\s*by",                             # "Emmet Avatarby" byline
    r"Updated",
    r"Favorite",
    r"[A-Z][a-z]{2,9}\.?\s+\d{1,2},?\s+\d{4}",    # standalone date line ("Jun 16, 2024")
]
_JUNK_RE = [re.compile(rf"^{p}$", re.IGNORECASE) for p in _JUNK_LINE_PATTERNS]


def _strip_entities(text):
    for k, v in _HTML_ENTITIES.items():
        text = text.replace(k, v)
    return text


def clean_text(text):
    """Remove boilerplate lines, decode HTML entities, dedupe repeated paragraphs."""
    text = _strip_entities(text)

    # Drop junk lines.
    kept = [ln for ln in text.splitlines()
            if not any(rx.match(ln.strip()) for rx in _JUNK_RE)]
    cleaned = "\n".join(kept)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    # Dedupe long duplicate paragraphs (forums repeat the accepted answer / quote prior posts).
    seen, paragraphs = set(), []
    for para in (p.strip() for p in cleaned.split("\n\n")):
        if not para:
            continue
        if len(para) > 80 and para in seen:
            continue
        seen.add(para)
        paragraphs.append(para)

    cleaned = "\n\n".join(paragraphs)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    return cleaned.strip()


# --------------------------------------------------------------------------- #
# Stage 3: chunk (recursive, structure-aware)
# --------------------------------------------------------------------------- #
_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]


def _recursive_split(text, separators, size):
    """Break text into atomic pieces, each <= size where the separators allow."""
    sep, remaining = separators[0], separators[1:]
    if sep == "":                                  # last resort: hard character cut
        return [text[i:i + size] for i in range(0, len(text), size)]

    pieces, result = text.split(sep), []
    for piece in pieces:
        piece = piece.strip()
        if not piece:
            continue
        if len(piece) <= size:
            result.append(piece)
        else:
            result.extend(_recursive_split(piece, remaining, size))
    return result


def _merge_with_overlap(splits, size, overlap):
    """Greedily merge small pieces up to `size`, carrying a word-aligned overlap tail."""
    chunks, current = [], ""
    for s in splits:
        if current and len(current) + 1 + len(s) > size:
            chunks.append(current.strip())
            tail = current[-overlap:] if overlap else ""
            cut = tail.find(" ")                   # start overlap on a word boundary
            tail = tail[cut + 1:] if cut != -1 else tail
            current = (tail + " " + s).strip()
        else:
            current = f"{current} {s}".strip() if current else s
    if current.strip():
        chunks.append(current.strip())
    return chunks


def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split one cleaned document into overlapping, boundary-aware chunks."""
    splits = _recursive_split(text, _SEPARATORS, size)
    return [c for c in _merge_with_overlap(splits, size, overlap) if c.strip()]


# --------------------------------------------------------------------------- #
# Pipeline + inspection
# --------------------------------------------------------------------------- #
def build_chunks(docs_dir=DOCS_DIR):
    """Full pipeline: load -> clean -> chunk. Returns list of chunk dicts with metadata."""
    chunks = []
    for doc in load_documents(docs_dir):
        for i, text in enumerate(chunk_text(clean_text(doc["raw"]))):
            chunks.append({
                "id": f'{doc["source"]}::chunk{i}',
                "source": doc["source"],
                "chunk_index": i,
                "text": text,
            })
    return chunks


def _approx_tokens(text):
    return round(len(text) / 4)


def main():
    docs = load_documents()
    chunks = build_chunks()
    lengths = [len(c["text"]) for c in chunks]

    print(f"Documents loaded : {len(docs)}")
    print(f"Total chunks     : {len(chunks)}")
    print(f"Chunk chars      : min {min(lengths)} | "
          f"mean {round(statistics.mean(lengths))} | max {max(lengths)}")
    print(f"Max approx tokens: ~{_approx_tokens(max(chunks, key=lambda c: len(c['text']))['text'])} "
          f"(limit is 256; chars/4 estimate)")
    print("\nChunks per document:")
    per_doc = {}
    for c in chunks:
        per_doc[c["source"]] = per_doc.get(c["source"], 0) + 1
    for src in sorted(per_doc):
        print(f"  {src:<40} {per_doc[src]}")

    # Print 5 chunks spread across the corpus so samples come from different documents.
    print("\n" + "=" * 70 + "\n5 SAMPLE CHUNKS\n" + "=" * 70)
    step = max(1, len(chunks) // 5)
    for c in chunks[::step][:5]:
        print(f"\n[{c['id']}]  ({len(c['text'])} chars, ~{_approx_tokens(c['text'])} tokens)")
        print("-" * 70)
        print(c["text"])

    CHUNKS_OUT.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {len(chunks)} chunks -> {CHUNKS_OUT.name}")


if __name__ == "__main__":
    main()
