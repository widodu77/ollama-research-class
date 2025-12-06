# Llama Document Extraction

Quick project i had for uni (left .env.examlpe in here cause it lowkey dosen't have much in it)

this is a lightweight interface for extracting data from documents (CSV/PDF) using Llama3:8b via Ollama.

## What Does This Do?

This application lets you upload CSV or PDF documents and extract structured data using a local AI model (Llama3:8b). It consists of:
- **FastAPI Backend**: Handles document processing and communicates with Ollama
- **Streamlit Frontend**: Provides a clean web interface for uploading files and viewing results
- **Ollama Integration**: Runs the Llama3:8b model locally on your machine

## Prerequisites

**REQUIRED - This won't work without these:**

1. **[Ollama Desktop](https://ollama.com/download)** - Download and install
2. **Llama3:8b model** - After installing Ollama, run:
   ```bash
   ollama pull llama3:8b
   ```
3. **Python 3.12+** (this project uses uv which requires Python 3.12)
4. **[uv](https://docs.astral.sh/uv/)** - Python package manager

## Quick Start (Using uv)

### 1. Install uv (if you haven't already)

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies

```bash
uv sync
```

This installs all dependencies from `pyproject.toml` and creates a virtual environment automatically.

### 3. Verify Ollama is Running

Make sure Ollama Desktop is running and the model is available:

```bash
ollama list
```

You should see `llama3:8b` in the list. If not, run `ollama pull llama3:8b`.

### 4. Run the Application

**Terminal 1 - Start FastAPI Backend:**

```bash
uv run python backend.py
```

The API will be available at `http://127.0.0.1:8000`

**Terminal 2 - Start Streamlit Frontend:**

```bash
uv run streamlit run app.py
```

The UI will open automatically in your browser at `http://localhost:8501`

## Usage

1. Open the Streamlit interface in your browser
2. Upload a PDF or CSV file
3. (Optional) Enter a specific extraction query like:
   - "Extract all email addresses and phone numbers"
   - "Summarize the key points in bullet format"
   - "List all numerical data and their labels"
4. Click "Extract Data"
5. View the extracted information

## API Endpoints

### GET `/health`
Check API and Ollama connection status

### POST `/extract`
Extract data from uploaded document

**Parameters:**
- `file`: PDF or CSV file
- `query`: (Optional) Extraction instructions

### GET `/models`
List available Ollama models

## Project Structure

```
llama-research/
├── app.py              # Streamlit frontend
├── backend.py          # FastAPI backend
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
└── README.md          # This file
```

## Common Issues That Will Break This

### 1. Memory Errors / Out of Memory
**Symptom:** Application crashes with memory error during processing

**Causes:**
- Document is too large (very long PDFs or large CSV files)
- Extraction query/prompt is too long
- System doesn't have enough RAM for Llama3:8b

**Solutions:**
- Use smaller documents (try splitting large PDFs)
- Keep extraction queries concise and specific
- Close other applications to free up RAM
- Consider using a smaller model if you have limited RAM
- For Ollama, you can set memory limits in settings

### 2. Ollama Not Found / Model Not Available
**Symptom:** API returns "model not found" or connection errors

**Must Have:**
- Ollama Desktop must be installed AND running
- Llama3:8b model must be downloaded via `ollama pull llama3:8b`
- Verify with `ollama list` - you should see llama3:8b

## Example Queries

**For CSV files:**
- "Extract the top 5 rows and explain what each column represents"
- "Summarize the statistical trends in this data"


**For PDF files:**
- "Extract all contact information including names, emails, and phone numbers"
- "Summarize this document in 3 bullet points"
- "Find all dates and events mentioned"

