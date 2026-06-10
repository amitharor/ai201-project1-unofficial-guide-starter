"""
Milestone 5 — Grounded answer generation with source attribution.

ask(question) retrieves the top chunks, asks Groq's llama-3.3-70b to answer using ONLY
that context, and returns the answer plus the source documents it drew from.

Grounding is enforced three ways:
  1. A strict system prompt: answer only from context, else refuse with a fixed phrase.
  2. A relevance filter: chunks above MAX_DISTANCE are dropped, so an off-topic query
     reaches the model with no context and gets refused (often without an API call).
  3. Source attribution is appended programmatically from chunk metadata, not left to
     the model to invent.
"""

import os

from dotenv import load_dotenv
from groq import Groq

from embed import retrieve

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_DISTANCE = 0.75            # cosine distance above this = too weak to count as context
REFUSAL = "I don't have enough information on that."

SYSTEM_PROMPT = (
    "You are the Unofficial UniFi Guide, answering questions about UniFi home networking "
    "using community forum threads and blog guides.\n"
    "Rules:\n"
    "1. Answer using ONLY the information in the provided context. Do not use outside knowledge.\n"
    f"2. If the context does not contain enough information to answer, reply with exactly: "
    f"'{REFUSAL}'\n"
    "3. Do not invent model names, specs, numbers, or steps that are not in the context.\n"
    "4. Be concise and practical."
)

_client = None


def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def _format_context(chunks):
    return "\n\n".join(
        f"[{i}] (source: {c['source']})\n{c['text']}" for i, c in enumerate(chunks, 1)
    )


def _unique_sources(chunks):
    seen, ordered = set(), []
    for c in chunks:
        if c["source"] not in seen:
            seen.add(c["source"])
            ordered.append(c["source"])
    return ordered


def ask(question, k=5):
    """Return {answer, sources, chunks} grounded in retrieved context."""
    chunks = retrieve(question, k=k)
    relevant = [c for c in chunks if c["distance"] < MAX_DISTANCE]

    # No usable context -> refuse without calling the LLM.
    if not relevant:
        return {"answer": REFUSAL, "sources": [], "chunks": []}

    resp = get_client().chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": f"Context:\n{_format_context(relevant)}\n\nQuestion: {question}"},
        ],
    )
    answer = resp.choices[0].message.content.strip()

    # Don't attribute sources to a refusal.
    sources = [] if REFUSAL.lower() in answer.lower() else _unique_sources(relevant)
    return {"answer": answer, "sources": sources, "chunks": relevant}


if __name__ == "__main__":
    demo_questions = [
        "Does the UniFi Cloud Gateway Ultra have a built-in Wi-Fi access point?",
        "What PoE standard does a U7 Pro access point need to be powered?",
        "What's the best pizza place in Chicago?",   # out-of-scope -> should refuse
    ]
    for q in demo_questions:
        result = ask(q)
        print("\n" + "=" * 78)
        print("Q:", q)
        print("-" * 78)
        print(result["answer"])
        print("\nSources:", ", ".join(result["sources"]) if result["sources"] else "(none)")
