from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from src.vector_store import load_vector_store
from src.logger import get_logger

logger = get_logger(__name__)

def get_qa_chain(model_name: str = "llama3.2") -> RetrievalQA:
    logger.info(f"Initializing QA chain with model: {model_name}")
    
    try:
        llm = Ollama(model=model_name)
        vectordb = load_vector_store()
        retriever = vectordb.as_retriever()
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )
        logger.info("QA chain successfully initialized.")
        return qa_chain
    except Exception as e:
        logger.error(f"Error initializing QA chain: {e}")
        raise

def ask_question(query: str, model_name: str = "llama3.2"):
    logger.info(f"Received query: {query}")
    try:
        qa_chain = get_qa_chain(model_name=model_name)
        result = qa_chain.invoke({"query": query})

        answer = result["result"]
        sources = result["source_documents"]

        logger.info("Answer generated successfully.")
        logger.debug(f"Answer: {answer}")
        logger.debug(f"Number of source documents retrieved: {len(sources)}")

        retrieved_texts = "\n\n".join(
            f" Chunk {i+1}:\n{doc.page_content}" for i, doc in enumerate(sources)
        )

        return answer, retrieved_texts
    except Exception as e:
        logger.error(f"Error during question answering: {e}")
        raise