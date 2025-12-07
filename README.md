# ✨ LIRA | Local Intelligent Retrieval Agent

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Ollama](https://img.shields.io/badge/AI-Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)

> **"An AI Chatbot that runs 100% on your local hardware."**

## 🔮 What is LIRA?
**LIRA** (Local Intelligent Retrieval Agent) is a secure, offline RAG (Retrieval-Augmented Generation) application. It allows users to upload private documents (PDFs, TXT) and chat with them using a powerful AI model running entirely on their own laptop.

Unlike cloud-based tools (like ChatGPT), **LIRA ensures zero data leakage**. Your documents never leave your machine.

---

## 📸 Screenshots

<img src="Screenshot 2025-12-07 130950.png" alt="Screenshot" width="1000" height="800"/>

---

## 🚀 Key Features
* **🧠 Fully Local Intelligence:** Powered by **Ollama (Qwen 2.5: 1.5B)** for high-speed, offline inference.
* **🔒 Privacy by Default:** No API keys required. No cloud servers involved.
* **🎨 Aesthetic UI:** A futuristic "Midnight Aurora" interface featuring glassmorphism effects, 3D avatars, and animated gradients.
* **⚡ High Performance:** Optimized for standard laptops (8GB RAM) using **ChromaDB** for lightweight vector storage.
* **📂 Easy Ingestion:** Instantly memorizes PDFs and Text files for real-time Q&A.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Custom CSS for modern UI)
* **Backend:** FastAPI (Asynchronous API)
* **Vector Database:** ChromaDB (Persistent storage)
* **LLM Orchestration:** LangChain
* **AI Engine:** Ollama

---

## 💻 How to Run Locally

### 1. Prerequisites
Ensure you have [Python 3.10+](https://www.python.org/) and [Ollama](https://ollama.com/) installed.

### 2. Clone the Repository
```bash
git clone https://github.com/Niranjana261102/LIRA-Local-Intelligent-Retrieval-Agent.git
cd LIRA-Local-Intelligent-Retrieval-Agent
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Setup the AI Brain
Run these commands in your terminal to download the models:
```bash
ollama pull qwen2.5:1.5b
ollama pull nomic-embed-text
```
### 5. Launch the Application
Terminal 1 (Backend):
```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000
```
Terminal 2 (Frontend):
```bash
streamlit run ui.py
```

