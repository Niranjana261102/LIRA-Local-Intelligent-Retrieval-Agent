from .llm import LocalLLM
from sentence_transformers import SentenceTransformer
import weaviate

EMBED_MODEL = "all-MiniLM-L6-v2"
WEAVIATE_CLASS = "DocumentChunk"

class HyDE:
    def __init__(self, weaviate_url: str = "http://localhost:8080", llm_model: str = None):
        self.client = weaviate.Client(weaviate_url)
        self.embedder = SentenceTransformer(EMBED_MODEL)
        self.llm = LocalLLM(model_name=llm_model) if llm_model else LocalLLM()

    def retrieve_with_hyde(self, query: str, top_k: int = 5):
        # generate hypothetical document
        pseudo_doc = self.llm.answer(query, contexts=[], max_length=150)
        # combine query+pseudo_doc into single embedding
        combined = query + "\n" + pseudo_doc
        qvec = self.embedder.encode([combined])[0].tolist()
        res = self.client.query.get(WEAVIATE_CLASS, ["text", "source"]).with_near_vector({"vector": qvec}).with_limit(top_k).do()
        out = []
        if res and "data" in res and "Get" in res["data"]:
            items = res["data"]["Get"].get(WEAVIATE_CLASS, [])
            for item in items:
                out.append({"text": item.get("text"), "source": item.get("source")})
        return out
