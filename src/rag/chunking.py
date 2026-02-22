# src/rag/chunking.py

from __future__ import annotations

def chunk_text(text: str, max_chars: int = 900, overlap: int = 120) -> list[str]:
    """
    Simple chunker:
    - splits on blank lines (paragraphs)
    - packs paragraphs into chunks up to max_chars
    - adds small overlap for continuity
    """
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    buf: list[str] = []
    buf_len = 0

    for p in paras:
        if buf_len + len(p) + 2 <= max_chars:
            buf.append(p)
            buf_len += len(p) + 2
            continue

        if buf:
            chunk = "\n\n".join(buf)
            chunks.append(chunk)

            # overlap: keep last N chars from previous chunk as prefix for next
            tail = chunk[-overlap:] if overlap > 0 else ""
            buf = [tail, p] if tail else [p]
            buf_len = len("\n\n".join(buf))
        else:
            # paragraph itself too big: hard split
            for i in range(0, len(p), max_chars):
                chunks.append(p[i:i+max_chars])

            buf = []
            buf_len = 0

    if buf:
        chunks.append("\n\n".join(buf))

    return chunks