from .retrieval import Retriever
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Evaluator:
    def __init__(self, weaviate_url="http://localhost:8080"):
        self.retriever = Retriever(weaviate_url=weaviate_url)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def retrieval_accuracy(self, tests: list, top_k=5):
        """
        tests: list of dicts: {"query": str, "expected_source": "<filename or label>"}
        """
        hits = 0
        for t in tests:
            retrieved = self.retriever.retrieve(t["query"], top_k=top_k)
            sources = [r["source"] for r in retrieved]
            if t["expected_source"] in sources:
                hits += 1
        return hits / len(tests)

    def contextual_precision(self, tests: list, top_k=5):
        """
        For each test, generate embedding of expected answer (if provided) and calculate
        avg top-k cosine similarity between expected answer and retrieved chunks.
        tests: [{"query":..., "expected_answer": "..."}]
        """
        scores = []
        for t in tests:
            retrieved = self.retriever.retrieve(t["query"], top_k=top_k)
            if not retrieved:
                scores.append(0.0)
                continue
            retrieved_texts = [r["text"] for r in retrieved]
            emb_expected = self.embedder.encode([t["expected_answer"]])[0]
            emb_rets = self.embedder.encode(retrieved_texts)
            sims = cosine_similarity([emb_expected], emb_rets)[0]
            scores.append(float(np.mean(sims)))
        return float(np.mean(scores))
