from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional, List 
import os

# Import bot engine dari file ai_engine.py
# Pastikan file ai_engine.py ada di folder yang sama
from ai_engine import ai_bot

# --- 1. LIFESPAN (Load Model saat Server Nyala) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model sebelum terima request biar user gak nunggu lama pas pertama chat
    ai_bot.load_models()
    yield
    # Code disini jalan pas server mati (cleanup)

# --- 2. INIT APP ---
app = FastAPI(title="AI GDrive Backend", lifespan=lifespan)

# --- 3. SCHEMAS (Struktur Data) ---

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "guest"

# Model khusus untuk menampung info file GDrive
class GDriveFile(BaseModel):
    filename: str
    gdrive_url: str
    gdrive_id: str
    preview: Optional[str] = None

# Response utama sekarang menampung list of files (ARRAY)
class ChatResponse(BaseModel):
    reply: str
    files: List[GDriveFile] = []  # Array kosong [] kalau gak ada file yg cocok
    folder_url: Optional[str] = None

# --- 4. API ENDPOINTS ---

@app.get("/")
def check_health():
    """Cek status server dan AI"""
    return {
        "status": "online", 
        "ai_ready": ai_bot.is_ready,
        "mode": "Multi-File Support"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint Chat Utama.
    Menerima pesan user -> Kirim ke AI -> Balikin jawaban text + List File GDrive
    """
    try:
        # 1. Panggil logic utama di ai_engine
        result = ai_bot.process_query(request.message)
        
        # 2. Cek error dari engine
        if "error" in result:
             raise HTTPException(status_code=503, detail=result["error"])
        
        # 3. Format response sesuai hasil temuan
        if result["found"]:
            return ChatResponse(
                reply=result["reply"],
                files=result["files"],         # List file dari AI Engine langsung masuk sini
                folder_url=result["gdrive_folder"]
            )
        else:
            # Kalau gak nemu, balikin reply aja, files kosong
            return ChatResponse(
                reply=result["reply"],
                files=[]
            )
            
    except Exception as e:
        print(f"Error di endpoint chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/file/list")
async def list_loaded_models():
    """
    Endpoint debug buat liat file model apa aja yang ada di folder ml_assets
    """
    try:
        if os.path.exists("ml_assets"):
            files = os.listdir("ml_assets")
            return {"status": "success", "files": files}
        return {"status": "warning", "message": "ml_assets folder not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))