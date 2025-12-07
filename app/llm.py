import os

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List

# We use Ollama because it is free, local, and fits in 8GB RAM
# Make sure you run 'ollama run qwen2.5:1.5b' in your terminal first
DEFAULT_MODEL = "qwen2.5:1.5b"


class LocalLLM:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.llm = ChatOllama(model=model_name)
        self.parser = StrOutputParser()

        ollama_base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")

        self.llm = ChatOllama(
            model=model_name,
            base_url=ollama_base_url  # <--- Add this line
        )

        # LangChain Prompt Template
        self.prompt = ChatPromptTemplate.from_template("""
        You are a helpful assistant. Answer the question based ONLY on the following context. 
        If the answer is not in the context, say "I don't know based on the provided documents."

        Context:
        {context}

        Question: {question}
        """)

    def answer(self, question: str, contexts: List[str]) -> str:
        # Join the list of retrieved text chunks into one string
        context_text = "\n\n".join(contexts)

        # Create the chain: Prompt -> LLM -> Text Output
        chain = self.prompt | self.llm | self.parser

        # Run the chain
        response = chain.invoke({"context": context_text, "question": question})
        return response