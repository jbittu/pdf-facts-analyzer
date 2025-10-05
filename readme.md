# PDF Facts Analyzer

A full-stack web application that extracts requested facts from a PDF document. Users can upload a PDF, specify pointers like “List all dates” or “Who signed?”, and receive structured results with snippets, page numbers, and rationales.

# 📂 Repository Structure
```bash
    pdf-facts-analyzer/
    │
    ├─ backend/               
    │  ├─ app/
    │  │  ├─ main.py          
    │  │  ├─ extractor.py     
    │  │  └─ models.py        
    │  ├─ uploads/            
    │  └─ requirements.txt
    │
    ├─ frontend/              
    │  ├─ pages/
    │  │  ├─ index.js
    │  │  └─ _app.js
    │  ├─ components/
    │  │  └─ Results.js       
    │  ├─ styles/
    │  │  ├─ globals.css
    │  │  └─ Home.css
    │  └─ package.json
    │
    └─ README.md
```

# 🚀 Features
## Backend (FastAPI)

Accepts PDF upload and JSON array of pointers.
Extracts text from text-based PDFs using PyMuPDF.
Returns for each pointer:
    Text snippet(s)
    Page number
    Character offset (start/end)
    Short rationale/explanation
Stores uploaded PDFs locally (or in-memory).

## Frontend (Next.js + Vanilla CSS)

Upload PDF and specify multiple pointers.
Submit button calls backend API.
Displays results per pointer:
    Snippets with page number
    Expandable to show context
Uses React functional components and a Results component for rendering output.
Clean, modern UI with glassmorphic form card and styled results.

# ⚙️ Setup Instructions
## 1️⃣ Backend Setup
```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
API docs: http://localhost:8000/docs

## 2️⃣ Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open in browser: http://localhost:3000

## 📝 Usage

1.Open frontend at http://localhost:3000
2.Upload a text-based PDF
3.Enter pointers (one per line), e.g.:
```bash
List all dates
Who signed?
Total contract value?
```
4.Click Analyze
5.View results in expandable cards with snippet, page number, offsets, and rationale.

## ⚡ Tech Stack
Backend: Python, FastAPI, PyMuPDF (fitz), Uvicorn
Frontend: Next.js, React Hooks, Vanilla CSS
State Management: React useState
Storage: Local uploads (can switch to cloud storage)
Communication: REST API (JSON)

## 🧩 Notes
Works only with text-based PDFs, not scanned images (no OCR).
Ensure backend is running at http://localhost:8000
 before using frontend.

## 🫱 Author
# Bittu Jaiswal – Full-stack developer & PDF enthusiast