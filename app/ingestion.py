import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# SETTINGS
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
PERSIST_DIRECTORY = "./chroma_db"  # Data is saved here

# Use Ollama for embeddings (running locally)
embeddings = OllamaEmbeddings(model="nomic-embed-text")


class Ingestor:
    def __init__(self):
        # Initialize the database connection
        self.vector_store = Chroma(
            collection_name="rag_collection",
            embedding_function=embeddings,
            persist_directory=PERSIST_DIRECTORY
        )

    def ingest_file(self, file_path: str):
        print(f"Processing {file_path}...")

        # 1. Load the file
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)

        docs = loader.load()

        # 2. Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        splits = text_splitter.split_documents(docs)

        # 3. Save to ChromaDB
        print(f"Saving {len(splits)} chunks to ChromaDB...")
        self.vector_store.add_documents(documents=splits)

        return len(splits)