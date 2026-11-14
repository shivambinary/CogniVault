from pathlib import Path

def parse_document(file_path: Path) -> dict:
    """This is read a document and return its content with basic source metadata."""

    text = file_path.read_text(
        encoding="utf-8",
        errors = "replace"
    ).strip()

    return {
        "source": file_path.name,
        "text": text
    }