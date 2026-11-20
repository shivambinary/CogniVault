import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "storage" / "processed"
OUTPUT_PATH = BASE_DIR / "storage" / "chunks" / "chunks.json"
CHUNK_WORDS = 150
OVERLAP_WORDS = 30


def split_text(text: str) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    while start < len(words):
        end = min(start + CHUNK_WORDS, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - OVERLAP_WORDS
    return chunks


def main() -> None:
    chunk_records = []
    documents = sorted(INPUT_DIR.glob("*.json"))
    if not documents:
        raise FileNotFoundError(f"No processed documents found in {INPUT_DIR}.")

    for document_path in documents:
        document = json.loads(document_path.read_text(encoding="utf-8"))
        source = document.get("source", document_path.stem)
        for index, text in enumerate(split_text(document.get("text", ""))):
            chunk_records.append(
                {
                    "id": f"{Path(source).stem}_chunk_{index:04d}",
                    "source": source,
                    "text": text,
                }
            )

    if not chunk_records:
        raise ValueError("No text found in processed documents.")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(chunk_records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Created {len(chunk_records)} chunks at {OUTPUT_PATH}.")


if __name__ == "__main__":
    main()
