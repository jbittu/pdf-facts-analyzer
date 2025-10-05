from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn
import json
import os
from .extractor import PDFExtractor

app = FastAPI(title="PDF Facts Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

extractor = PDFExtractor()

@app.post("/analyze")
async def analyze(pdf: UploadFile = File(...), pointers: str = Form(...)) -> Dict[str, Any]:
    """
    Expects:
      - pdf: uploaded file
      - pointers: JSON-encoded array of strings (textual pointers)
    Returns:
      - results: dict mapping each pointer to an array of matches
    """
    try:
        pointers_list = json.loads(pointers)
        if not isinstance(pointers_list, list):
            raise ValueError("pointers must be a JSON array of strings")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid pointers JSON: {e}")

    filename = os.path.basename(pdf.filename)
    save_path = os.path.join(UPLOAD_DIR, filename)
    content = await pdf.read()
    with open(save_path, "wb") as f:
        f.write(content)

    pages = extractor.extract_pages(save_path)

    results = {}
    for ptr in pointers_list:
        matches = extractor.handle_pointer(ptr, pages)
        results[ptr] = matches

    return {"file": filename, "results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)