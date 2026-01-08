# Context_flow

A FastAPI application for managing documents with Qdrant vector database.

## Project Structure

- `app/` - Backend application code
  - `main.py` - FastAPI application and endpoints
  - `qdrant.py` - Qdrant database operations
- `static/` - Static files
  - `index.html` - Frontend HTML page
- `tests/` - Test files
- `docs/` - Documentation
- `requirements.txt` - Python dependencies

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the server with:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000

Visit http://127.0.0.1:8000 to access the web interface for uploading Excel files and viewing stored documents.

## API Endpoints

- `POST /upload-excel` - Upload an Excel file to add records to Qdrant
- `GET /data` - Retrieve all stored data
- `GET /docs` - Interactive API documentation