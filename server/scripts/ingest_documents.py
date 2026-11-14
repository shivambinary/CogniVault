import json
from pathlib import Path

from ai.ingestion.parser import parse_document


BASE_DIR = Path(__file__).resolve().parents[1]

DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
OUTPUT_DIR = BASE_DIR / "storage" / "processed"


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    documents = list(DOCUMENTS_DIR.glob("*.txt"))

    if not documents:
        print("No documents found!")
        return

    for file_path in documents:

        document = parse_document(file_path)

        output_path = OUTPUT_DIR / f"{file_path.stem}.json"

        output_path.write_text(
            json.dumps(document, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

        print(f"Processed: {file_path.name}")

    print(f"\nSuccessfully processed {len(documents)} documents.")


if __name__ == "__main__":
    main()