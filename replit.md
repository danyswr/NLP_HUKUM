# NLP Hukum - AI Legal Document Assistant

## Overview
A full-stack application with a ChatGPT-style dashboard for searching legal documents in Google Drive. Uses NLP/AI to match user queries to relevant Indonesian legal documents (UU, Peraturan, etc).

## Project Structure
```
Backend/                    # Python FastAPI backend (port 8000)
  - main.py                 # Entry point, uvicorn server
  - api.py                  # FastAPI endpoints
  - ai_engine.py            # AI/NLP document matching logic
  - models-asset/           # Pre-trained models and metadata
  - ml_assets/              # Symlink to models-asset

frontend/                   # Next.js frontend (port 5000)
  - src/app/                # Next.js app router pages
  - src/components/         # React components (Sidebar, ChatArea)
  - src/types/              # TypeScript type definitions
```

## API Endpoints (Backend)
- `GET /` - Health check, returns AI status
- `POST /api/chat` - Main chat endpoint, returns matching documents
- `GET /api/file/list` - Debug endpoint for loaded models

## Running the Application
- Frontend (port 5000): `cd frontend && npm run dev`
- Backend (port 8000): `cd Backend && python main.py`

## Dependencies
### Backend (Python)
- FastAPI, Uvicorn, Pydantic, rank_bm25

### Frontend (Node.js)
- Next.js 14, React 18, Tailwind CSS

## Recent Changes
- 2024-12-13: Fixed AI model search flow - now uses BM25 on document content, returns up to 10 relevant files
- 2024-12-13: Added FileModal popup for document preview with download button
- 2024-12-13: Loaded dataset_bpk.csv (115 documents) for better semantic search
- 2024-12-13: Added Next.js frontend with ChatGPT-style dashboard
- 2024-12-13: Initial Replit setup
