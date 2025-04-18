import os

DATA_PATH = "data/ubuntu-docs"
VECTOR_STORE_PATH = "vector_store/faiss_index"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Ollama LLM Config
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:11434/v1")
Ollama_MODEL = "llama3.2"  