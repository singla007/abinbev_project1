import gradio as gr
from src.qa_bot import ask_question
from src.logger import get_logger

logger = get_logger(__name__)
demo = gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(label="Ask a question", placeholder="e.g., What is Ubuntu Core 20 built on?"),
    outputs=[
        gr.Textbox(label="🧠 Answer"),
        gr.Textbox(label="📄 Retrieved Chunks"),
    ],
    title="Ubuntu Q&A for ABInBev",
    description="Ask any question about the documents. The system retrieves relevant chunks and answers using Ollama LLM."
)

if __name__ == "__main__":
    demo.launch()