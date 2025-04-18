from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.config import *
from src.utils import load_markdown_files 
import os


def create_vector_store():

    docs = load_markdown_files(DATA_PATH)
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    
    chunks = []
    for path, content in docs:
        for chunk in splitter.split_text(content):
            chunks.append(chunk)

    print(f"[+] Total chunks: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = FAISS.from_texts(chunks, embedding=embeddings)

    vectordb.save_local(VECTOR_STORE_PATH)
    print(f"[+] Vector store saved at {VECTOR_STORE_PATH}")


def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if not os.path.exists(VECTOR_STORE_PATH):
        raise FileNotFoundError(f"Vector store not found at {VECTOR_STORE_PATH}. Run create_vector_store() first.")

    return FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)


def retrieve_similar_docs(query: str, k: int = 10):

    # Load the persisted vector store
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)

    # Perform similarity search
    results = vectordb.similarity_search(query, k=k)

    print(f"\n[?] Query: {query}")
    print(f"[+] Top {k} matched documents:\n")
    for i, doc in enumerate(results, start=1):
        print(f"{i}. {doc.page_content}\n{'-'*80}")
