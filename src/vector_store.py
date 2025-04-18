from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.config import *
from src.utils import load_markdown_files 
import os
from src.logger import get_logger

logger = get_logger(__name__)

def create_vector_store():
    logger.info("Starting vector store creation...")
    try:
        docs = load_markdown_files(DATA_PATH)
        logger.info(f"Loaded {len(docs)} markdown documents from {DATA_PATH}")

        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        logger.debug(f"Using RecursiveCharacterTextSplitter with chunk_size={CHUNK_SIZE}, chunk_overlap={CHUNK_OVERLAP}")

        chunks = []
        for path, content in docs:
            chunked_texts = splitter.split_text(content)
            logger.debug(f"{len(chunked_texts)} chunks created from {path}")
            chunks.extend(chunked_texts)

        logger.info(f"Total chunks created: {len(chunks)}")

        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vectordb = FAISS.from_texts(chunks, embedding=embeddings)

        vectordb.save_local(VECTOR_STORE_PATH)
        logger.info(f"Vector store saved successfully at: {VECTOR_STORE_PATH}")

        return {
            "status": "success",
            "message": f"Vector store created with {len(chunks)} chunks",
            "saved_at": VECTOR_STORE_PATH }

    except Exception as e:
        logger.error(f"Error occurred during vector store creation: {e}", exc_info=True)
        raise


def load_vector_store():
    logger.info(f"Loading vector store from: {VECTOR_STORE_PATH}")
    try:
        if not os.path.exists(VECTOR_STORE_PATH):
            msg = f"Vector store not found at {VECTOR_STORE_PATH}. Run create_vector_store() first."
            logger.error(msg)
            raise FileNotFoundError(msg)

        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vectordb = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)

        logger.info("Vector store loaded successfully.")
        return vectordb

    except Exception as e:
        logger.error(f"Failed to load vector store: {e}", exc_info=True)
        raise


def retrieve_similar_docs(query: str, k: int = 10):
    logger.info(f"Performing similarity search for query: '{query}' with top-{k} results")

    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vectordb = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)

        results = vectordb.similarity_search(query, k=k)
        logger.info(f"{len(results)} results retrieved.")

        print(f"\n[?] Query: {query}")
        print(f"[+] Top {k} matched documents:\n")
        for i, doc in enumerate(results, start=1):
            print(f"{i}. {doc.page_content}\n{'-'*80}")

    except Exception as e:
        logger.error(f"Error during document retrieval: {e}", exc_info=True)
        raise