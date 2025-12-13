import uvicorn
import os

# File ini adalah pintu masuk (Entry Point) aplikasi.
# Jalankan file ini untuk menyalakan server:
# python main.py

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting AI Server on port {port}...")
    print("📂 Pastikan folder 'ml_assets' dan file 'ai_engine.py' sudah siap.")
    
    # 'api:app' merujuk ke:
    # api -> nama file api.py
    # app -> nama variable app = FastAPI(...) di dalam file tersebut
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)