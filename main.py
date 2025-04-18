# from src.vector_store import *
# from src.qa_bot import ask_question
# from src.logger import get_logger

# logger = get_logger(__name__)

# if __name__ == "__main__":
#     # create_vector_store()

#     # vectordb = load_vector_store()
#     # retrieve_similar_docs("How do I troubleshoot a failing Ubuntu package install?")
#     print(ask_question("what is foundation on which Ubuntu Core 20 is built"))
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Tuple
from src.qa_bot import ask_question
from src.logger import get_logger

app = FastAPI(
    title="Ubuntu Q&A Bot API",
    description="Ask questions related to Ubuntu documentation",
    version="1.0.0"
)

logger = get_logger(__name__)

class QAResponse(BaseModel):
    answer: str
    retrieved_chunks: str

@app.get("/ask", response_model=QAResponse)
def get_answer(query: str = Query(..., description="Your question for the QA bot")):
    """
    Ask a question about Ubuntu-related content and get an AI-generated answer with relevant document chunks.
    """
    try:
        logger.info(f"Received query: {query}")
        answer, sources = ask_question(query)
        print(answer)
        logger.info("Query processed successfully.")
        return QAResponse(answer=answer, retrieved_chunks=sources)
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        return {"answer": "An error occurred while processing the question.", "retrieved_chunks": ""}
    