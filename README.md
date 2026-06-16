# 📚 RAG Notes Assistant

A RAG (Retrieval Augmented Generation) based study assistant that lets you 
upload your notes or documents and ask questions about them in natural language.
Built with LangChain, FAISS, and Google Gemini.

## What it does
- Upload any PDF or TXT file (lecture notes, textbooks, solution sheets)
- Ask questions and get answers grounded in YOUR notes
- Hit "Quiz Me!" to auto-generate practice questions from your notes
- Answers are always based on your document — not general AI knowledge

## How it's different from just asking ChatGPT
Regular AI answers from general training data. This agent answers from YOUR 
specific notes. If something isn't in your notes, it tells you honestly.

## Tech Stack
- **LangChain + LangGraph** — Agent framework
- **Google Gemini 2.5 Flash** — LLM for answer generation
- **FAISS** — Local vector database for semantic search
- **HuggingFace (all-MiniLM-L6-v2)** — Local embedding model (no API needed)
- **Streamlit** — Web UI

## Project Structure
rag-notes-assistant/
├── .env               # API keys (not uploaded to GitHub)
├── ingest.py          # Reads documents, creates embeddings, stores in FAISS
├── retriever.py       # Searches vector database for relevant chunks
├── agent.py           # LangChain agent that answers questions
├── app.py             # Streamlit UI
└── requirements.txt

## Setup & Installation

1. Clone the repository
```bash
   git clone https://github.com/ravikumar49/rag-notes-assistant
   cd rag-notes-assistant
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file in the root folder

GEMINI_API_KEY=your_gemini_api_key_here

4. Run the app
```bash
   streamlit run app.py
```

## How to get API keys
- **Gemini API** — [Google AI Studio](https://aistudio.google.com)
- No API key needed for embeddings — runs locally on your machine!

## How RAG works in this project
Your PDF/TXT file
↓
Split into chunks (ingest.py)
↓
Each chunk → vector embedding (HuggingFace model, runs locally)
↓
Stored in FAISS vector database on disk
↓
User asks a question
↓
Question → vector (same embedding model)
↓
FAISS finds 3 most similar chunks (semantic search)
↓
Chunks + question sent to Gemini
↓
Gemini generates answer based on YOUR notes

## Key Concepts Demonstrated
- **RAG Pipeline** — Full implementation from ingestion to retrieval to generation
- **Vector Embeddings** — Converting text to numerical vectors that capture meaning
- **Semantic Search** — Finding relevant content by meaning, not just keywords
- **Local Vector Database** — FAISS running entirely on your machine
- **Agentic Tool Use** — LangChain agent deciding when and how to search notes

## Features
- Supports PDF and TXT files
- Automatic re-indexing when a new file is uploaded
- Quiz generation from your notes
- Honest responses — tells you when information isn't in your notes

## Screenshots
<img width="1920" height="951" alt="Screenshot (1222)" src="https://github.com/user-attachments/assets/d31cd533-d6d0-4663-8599-51fba9f97f9f" />


## Note
The `faiss_index/` folder is generated locally and not included in this 
repository. It will be created automatically when you upload your first document.
