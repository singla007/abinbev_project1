from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from src.vector_store import load_vector_store

def get_qa_chain(model_name: str = "llama3.2") -> RetrievalQA:
    llm = Ollama(model=model_name)
    vectordb = load_vector_store()
    retriever = vectordb.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

def ask_question(query: str, model_name: str = "llama3.2"):
    qa_chain = get_qa_chain(model_name=model_name)
    result = qa_chain.invoke({"query": query})

    answer = result["result"]
    sources = result["source_documents"]
    # print("\n Answer:")
    # print(result["result"])

    # print("\n📄 Retrieved Documents:")
    # for i, doc in enumerate(result["source_documents"], 1):
    #     print(f"\n--- Document {i} ---")
    #     print(doc.page_content)
    #     if doc.metadata:
    #         print("Metadata:", doc.metadata)

    retrieved_texts = "\n\n".join(
        f"🔹 Chunk {i+1}:\n{doc.page_content}" for i, doc in enumerate(sources)
    )

    return answer, retrieved_texts
