import os
import json
import pickle
import warnings
import random

# Library AI (Uncomment kalau sudah install)
# import torch
# import faiss
# import numpy as np

warnings.filterwarnings("ignore")

ASSETS_DIR = "ml_assets"
GDRIVE_FOLDER_ID = "1vYRLxyfqQSV_tJmTcXx423I5AacxFJOQ"

class AIEngine:
    def __init__(self):
        self.tokenizer = None
        self.index = None
        self.chunks = None
        self.file_names = []
        self.is_ready = False

    def load_models(self):
        print(f"🔄 Memulai proses loading model dari '{ASSETS_DIR}'...")
        try:
            # 1. Load Metadata
            meta_path = os.path.join(ASSETS_DIR, "metadata.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    raw_metadata = json.load(f)
                # file_names is a list, convert to usable format
                self.file_names = raw_metadata.get("file_names", [])
                print(f"✅ Metadata loaded - {len(self.file_names)} dokumen")
            else:
                self.file_names = []
                print("⚠️ Metadata tidak ditemukan.")

            # Load model lain...
            chunks_path = os.path.join(ASSETS_DIR, "chunks.pkl")
            if os.path.exists(chunks_path):
                with open(chunks_path, "rb") as f:
                    self.chunks = pickle.load(f)
                print(f"✅ Chunks loaded")

            self.is_ready = True
            print("🚀 AI Engine siap!")
        except Exception as e:
            print(f"❌ Error loading: {str(e)}")
            self.is_ready = False

    def predict_filename(self, user_message: str) -> list:
        """
        Cari file berdasarkan keyword dalam user message.
        Mencocokkan dengan daftar file dari metadata.
        """
        user_message = user_message.lower()
        found_files = []
        
        # Ekstrak keywords dari message
        keywords = user_message.replace("cari", "").replace("tentang", "").replace("dokumen", "").split()
        keywords = [k.strip() for k in keywords if len(k) > 2]
        
        # Cari file yang cocok dengan keyword
        for filename in self.file_names:
            filename_lower = filename.lower()
            for keyword in keywords:
                if keyword in filename_lower:
                    if filename not in found_files:
                        found_files.append(filename)
                    break
        
        # Limit hasil maksimal 5 file
        return found_files[:5]

    def get_gdrive_link(self, filename: str):
        """
        Mengambil link berdasarkan nama file.
        Catatan: Metadata saat ini hanya berisi list nama file tanpa individual GDrive ID.
        Untuk production, perlu ditambahkan mapping filename -> gdrive_id di metadata.json
        """
        if filename not in self.file_names:
            return None, None
        
        # Encode filename untuk URL search di Google Drive folder
        encoded_name = filename.replace(" ", "+")
        search_url = f"https://drive.google.com/drive/folders/{GDRIVE_FOLDER_ID}?q={encoded_name}"
        
        # Generate unique ID dari filename
        import hashlib
        file_id = hashlib.md5(filename.encode()).hexdigest()[:12]
        
        return file_id, search_url

    def process_query(self, user_message: str):
        """
        Main logic: Chat -> List of Files -> List of GDrive Links
        """
        if not self.is_ready:
            return {"error": "AI not ready"}

        # 1. Dapat list file dari model
        predicted_filenames = self.predict_filename(user_message)

        if not predicted_filenames:
            return {
                "found": False,
                "reply": "Maaf, saya tidak menemukan dokumen yang relevan di Google Drive."
            }

        # 2. Loop setiap file untuk cari Link GDrive-nya
        results = []
        for fname in predicted_filenames:
            file_id, gdrive_link = self.get_gdrive_link(fname)
            if file_id:
                results.append({
                    "filename": fname,
                    "gdrive_id": file_id,
                    "gdrive_url": gdrive_link
                })
        
        # Kalau ternyata dari sekian nama, gak ada satupun yang punya ID di metadata
        if not results:
             return {
                "found": False,
                "reply": f"Model menyarankan {predicted_filenames}, tapi file-file tersebut tidak ada di mapping GDrive."
            }

        # 3. Siapkan response sukses dengan list file
        file_count = len(results)
        if file_count == 1:
            reply = f"Saya menemukan 1 dokumen yang cocok: {results[0]['filename']}"
        else:
            file_list_str = ", ".join([r['filename'] for r in results[:3]])
            if file_count > 3:
                reply = f"Saya menemukan {file_count} dokumen yang cocok, termasuk: {file_list_str}, dan lainnya."
            else:
                reply = f"Saya menemukan {file_count} dokumen yang cocok: {file_list_str}"
        
        return {
            "found": True,
            "files": results,
            "gdrive_folder": f"https://drive.google.com/drive/folders/{GDRIVE_FOLDER_ID}",
            "reply": reply
        }

ai_bot = AIEngine()