from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


def split_blocks(text: str) -> list[str]:
    return [block.strip() for block in text.split("\n\n") if block.strip()]


@dataclass(frozen=True)
class ChunkEntry:
    chunk_id: str
    text: str
    source: str


def iter_chunks(data_dir: Path, extensions: Iterable[str]) -> list[ChunkEntry]:
    chunks: list[ChunkEntry] = []
    for path in data_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in extensions:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="ignore")

        for index, block in enumerate(split_blocks(text)):
            chunk_id = f"{path}:{index}"
            chunks.append(ChunkEntry(chunk_id=chunk_id, text=block, source=str(path)))
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Chroma vector index from local docs.")
    parser.add_argument("--data-dir", default="data", help="Directory with knowledge files")
    parser.add_argument("--extensions", default=".txt,.md", help="Comma-separated extensions")
    parser.add_argument("--chroma-path", default="data/chroma", help="Chroma persistence path")
    parser.add_argument("--collection", default="knowledge", help="Chroma collection name")
    parser.add_argument("--model", default="BAAI/bge-m3", help="SentenceTransformer model")
    parser.add_argument("--batch-size", type=int, default=64, help="Embedding batch size")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate collection")
    args = parser.parse_args()

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise SystemExit(
            "Missing dependencies. Install chromadb and sentence-transformers first."
        ) from exc

    data_dir = Path(args.data_dir)
    extensions = tuple(ext.strip() for ext in args.extensions.split(",") if ext.strip())

    client = chromadb.PersistentClient(path=str(args.chroma_path))
    if args.reset:
        try:
            client.delete_collection(args.collection)
        except ValueError:
            pass
    collection = client.get_or_create_collection(
        name=args.collection,
        metadata={"hnsw:space": "cosine"},
    )

    model = SentenceTransformer(args.model)
    chunks = iter_chunks(data_dir, extensions)
    if not chunks:
        print("No chunks found. Check data directory and extensions.")
        return

    texts = [chunk.text for chunk in chunks]
    ids = [chunk.chunk_id for chunk in chunks]
    metadatas = [{"source": chunk.source} for chunk in chunks]

    for start in range(0, len(texts), args.batch_size):
        batch_texts = texts[start : start + args.batch_size]
        batch_ids = ids[start : start + args.batch_size]
        batch_meta = metadatas[start : start + args.batch_size]
        embeddings = model.encode(batch_texts, normalize_embeddings=True).tolist()
        collection.upsert(
            ids=batch_ids,
            documents=batch_texts,
            embeddings=embeddings,
            metadatas=batch_meta,
        )

    print(f"Indexed {len(texts)} chunks into '{args.collection}'.")


if __name__ == "__main__":
    main()
