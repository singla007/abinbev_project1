import os
from pathlib import Path

def load_markdown_files(data_path):
    md_files = list(Path(data_path).rglob("*.md"))
    documents = []
    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            documents.append((str(file_path), f.read()))
    return documents