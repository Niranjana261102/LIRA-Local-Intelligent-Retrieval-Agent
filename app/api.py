import os
from fastapi import FastAPI, UploadFile, File, Form
from app.ingestion import Ingestor
from app.retrieval import Retriever
from app.llm import LocalLLM

app = FastAPI(title="LIRA - Local RAG Agent")

# Initialize our components (No arguments needed now!)
ingestor = Ingestor()
retriever = Retriever()
llm = LocalLLM()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    save_path = f"./data/{file.filename}"
    os.makedirs("./data", exist_ok=True)

    # Save file to disk
    with open(save_path, "wb") as f:
        f.write(await file.read())

    # Ingest
    try:
        count = ingestor.ingest_file(save_path)
        return {"message": "File ingested", "chunks": count}
    except Exception as e:
        return {"error": str(e)}


@app.post("/query")
async def query(q: str = Form(...)):
    # 1. Retrieve
    retrieved_docs = retriever.retrieve(q)

    # 2. Generate Answer
    contexts = [doc["text"] for doc in retrieved_docs]
    answer = llm.answer(q, contexts)

    return {"answer": answer, "sources": retrieved_docs}