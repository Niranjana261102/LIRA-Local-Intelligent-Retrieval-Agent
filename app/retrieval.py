from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

PERSIST_DIRECTORY = "./chroma_db"


class Retriever:
    def __init__(self):
        # We load the "Translator" (Embeddings) ONLY ONCE because it is heavy/slow
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

    def retrieve(self, query: str, top_k: int = 5):
        # We connect to the Database (Chroma) EVERY TIME a question is asked.
        # This ensures we see the latest files you just uploaded.
        vector_store = Chroma(
            collection_name="rag_collection",
            embedding_function=self.embeddings,
            persist_directory=PERSIST_DIRECTORY
        )

        # Search for relevant documents
        results = vector_store.similarity_search(query, k=top_k)

        return [{"text": doc.page_content, "source": doc.metadata.get("source", "unknown")} for doc in results]