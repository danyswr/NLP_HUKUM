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
        self.metadata = None  # Kita pake ini buat mapping Filename -> GDrive ID
        self.is_ready = False

    def load_models(self):
        print(f"🔄 Memulai proses loading model dari '{ASSETS_DIR}'...")
        try:
            # 1. Load Metadata (Mapping GDrive)
            meta_path = os.path.join(ASSETS_DIR, "metadata.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    self.metadata = json.load(f)
                print("✅ Metadata (Mapping GDrive) loaded")
            else:
                self.metadata = {
                    "laporan_keuangan.pdf": "12345_dummy_id_laporan",
                    "sop_perusahaan.docx": "67890_dummy_id_sop",
                    "data_karyawan.xlsx": "abcde_dummy_id_karyawan"
                }
                print("⚠️ Metadata tidak ditemukan, menggunakan Dummy Data.")

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
        Fungsi ini mengembalikan LIST nama file.
        Bisa 0, 1, atau banyak file tergantung deteksi model.
        """
        # --- LOGIC AI ASLI (Nanti uncomment) ---
        # input_ids = self.tokenizer(user_message)
        # predicted_labels = self.model(input_ids) # Pastikan model return list/multilabel
        # filenames = [self.label_decoder(lbl) for lbl in predicted_labels]
        # return filenames
        
        # --- LOGIC DUMMY (Support Multi-File) ---
        user_message = user_message.lower()
        found_files = []
        
        # Cek keyword satu per satu (bisa trigger banyak sekaligus)
        if "keuangan" in user_message or "duit" in user_message:
            found_files.append("laporan_keuangan.pdf")
        
        if "sop" in user_message or "aturan" in user_message:
            found_files.append("sop_perusahaan.docx")
            
        if "karyawan" in user_message:
            found_files.append("data_karyawan.xlsx")
            
        return found_files

    def get_gdrive_link(self, filename: str):
        """
        Mengambil link download/view berdasarkan nama file.
        """
        if not self.metadata or filename not in self.metadata:
            return None, None

        file_id = self.metadata[filename]
        view_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
        
        return file_id, view_link

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
        file_list_str = ", ".join([r['filename'] for r in results])
        
        return {
            "found": True,
            "files": results, # Return List of Objects
            "gdrive_folder": f"https://drive.google.com/drive/folders/{GDRIVE_FOLDER_ID}",
            "reply": f"Saya menemukan beberapa file yang cocok: {file_list_str}"
        }

ai_bot = AIEngine()