# NLP Hukum - AI GDrive Backend

## Overview
A FastAPI-based AI backend for searching and retrieving legal documents from Google Drive. The system uses NLP techniques to match user queries to relevant legal documents.

## Project Structure
```
Backend/
  - main.py         # Entry point, starts uvicorn server on port 5000
  - api.py          # FastAPI endpoints
  - ai_engine.py    # AI/NLP logic for document matching
  - models-asset/   # Pre-trained models and document metadata
  - ml_assets/      # Symlink to models-asset
```

## API Endpoints
- `GET /` - Health check, returns AI status
- `POST /api/chat` - Main chat endpoint, accepts message and returns matching documents
- `GET /api/file/list` - Debug endpoint to list loaded models

## Running the Application
The server runs on port 5000 using the command:
```
cd Backend && python main.py
```

## Dependencies
- FastAPI
- Uvicorn
- Pydantic
- rank_bm25

## Recent Changes
- 2024-12-13: Initial Replit setup, configured for port 5000
