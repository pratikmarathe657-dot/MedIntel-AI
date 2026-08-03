# 🩺 MedIntel AI

> **AI-Powered Medical Intelligence Platform**

MedIntel AI is an intelligent healthcare assistant that enables users to upload medical reports and interact with them using natural language. The platform leverages Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) to provide context-aware medical insights while also supporting general medical reasoning when report-specific information is unavailable.

---

# 🚀 Features

✅ Secure User Authentication

- User Registration
- User Login
- Session-based authentication

---

✅ Medical Report Upload

- Upload PDF medical reports
- Automatic text extraction
- Intelligent document processing

---

✅ AI-Powered Medical Q&A

- Ask questions about uploaded reports
- Context-aware answers using semantic search
- Medical reasoning for general healthcare queries

---

✅ Retrieval-Augmented Generation (RAG)

- PDF Text Extraction
- Text Chunking
- Embedding Generation
- Vector Similarity Search
- LLM-powered Response Generation

---

✅ Persistent Chat History

- Individual chat sessions
- Multiple reports
- SQLite-based storage

---

✅ Modern User Interface

- Responsive design
- Medical-themed UI
- Healthcare background
- Report history sidebar

---

# 🏗️ Project Architecture

```
Medical Report (PDF)
        │
        ▼
PDF Text Extraction
        │
        ▼
Text Chunking
        │
        ▼
Sentence Embeddings
        │
        ▼
Chroma Vector Database
        │
        ▼
Semantic Retrieval
        │
        ▼
Groq Llama 3.3
        │
        ▼
Medical AI Response
```

---

# ⚙️ Tech Stack

### Backend

- Python
- FastAPI

### Database

- SQLAlchemy

### AI & NLP

- Retrieval-Augmented Generation (RAG)
- ChromaDB
- Sentence Transformers
- Groq API
- Llama 3.3 70B

### Frontend

- HTML
- CSS
- JavaScript

---

# 📂 Project Structure

```
backend
│
├── services
│   ├── auth_service.py
│   ├── chunk_service.py
│   ├── embedding_service.py
│   ├── history_service.py
│   ├── llm_services.py
│   ├── pdf_service.py
│   ├── rag_service.py
│   ├── retrieval_service.py
│   └── vector_db.py
│
├── static
│   ├── css
│   ├── images
│   └── js
│
├── templates
│   ├── login.html
│   ├── register.html
│   └── index.html
│
├── database.py
├── models.py
├── gemini.py
├── main.py
├── requirements.txt
└── README.md
```


# 💡 How It Works

1. User registers and logs into the platform.
2. A medical report (PDF) is uploaded.
3. The system extracts and chunks the document.
4. Text embeddings are generated using Sentence Transformers.
5. Embeddings are stored in ChromaDB.
6. Relevant context is retrieved based on the user's query.
7. Groq Llama 3.3 generates a context-aware response.
8. Chat history is stored in SQLite for future reference.

---

# 🎯 Key Highlights

- AI-powered Medical Intelligence Platform
- Retrieval-Augmented Generation (RAG)
- FastAPI-based backend
- SQLite database integration
- Secure user authentication
- Persistent conversation history
- Semantic document retrieval
- Modern responsive interface

---

# 🚀 Future Enhancements

- OCR support for scanned medical reports
- Voice-based interaction
- Multi-document analysis
- Medical image interpretation
- Doctor dashboard
- Patient timeline
- Report comparison
- Multi-language support
- Cloud deployment
- Export AI-generated summaries

---

# ⭐ If you found this project interesting

Please consider giving it a ⭐ on GitHub.
