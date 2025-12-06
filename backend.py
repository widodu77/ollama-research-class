from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import ollama
import os
from dotenv import load_dotenv
import PyPDF2
import pandas as pd
import io
from typing import Optional

load_dotenv()

app = FastAPI(title="Llama Document Extraction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")


def extract_text_from_pdf(file_content: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_text_from_csv(file_content: bytes) -> str:
    df = pd.read_csv(io.BytesIO(file_content))
    return df.to_string()


@app.get("/")
async def root():
    return {"message": "Llama Document Extraction API", "model": OLLAMA_MODEL}


@app.get("/health")
async def health_check():
    try:
        ollama.list()
        return {"status": "healthy", "ollama": "connected", "model": OLLAMA_MODEL}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.post("/extract")
async def extract_data(
    file: UploadFile = File(...),
    query: Optional[str] = Form(None)
):
    try:
        file_content = await file.read()
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension == "pdf":
            document_text = extract_text_from_pdf(file_content)
        elif file_extension == "csv":
            document_text = extract_text_from_csv(file_content)
        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported file type: {file_extension}. Only PDF and CSV are supported."}
            )

        if not query:
            query = "Extract and summarize the key information from this document."

        prompt = f"""You are a data extraction assistant. Analyze the following document and {query}

Document content:
{document_text}

Please provide a clear, structured response with the extracted information."""

        response = ollama.generate(model=OLLAMA_MODEL, prompt=prompt)

        return {
            "success": True,
            "filename": file.filename,
            "file_type": file_extension,
            "query": query,
            "extraction": response["response"],
            "document_preview": document_text[:500] + "..." if len(document_text) > 500 else document_text
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/models")
async def list_models():
    try:
        models = ollama.list()
        return {"models": models}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("FASTAPI_HOST", "127.0.0.1")
    port = int(os.getenv("FASTAPI_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
