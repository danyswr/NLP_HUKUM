import os
import json
import pickle
import warnings

warnings.filterwarnings("ignore")

ASSETS_DIR = "models-asset"
GDRIVE_FOLDER_ID = "1vYRLxyfqQSV_tJmTcXx423I5AacxFJOQ"

class AIEngine:
    def __init__(self):
        self.bm25 = None
        self.chunks = None
        self.file_names = []
        self.is_ready = False

    def load_models(self):
        print(f"🔄 Memulai proses loading model dari '{ASSETS_DIR}'...")
        try:
            meta_path = os.path.join(ASSETS_DIR, "metadata.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    raw_metadata = json.load(f)
                self.file_names = raw_metadata.get("file_names", [])
                print(f"✅ Metadata loaded - {len(self.file_names)} dokumen")
            else:
                self.file_names = []
                print("⚠️ Metadata tidak ditemukan.")

            chunks_path = os.path.join(ASSETS_DIR, "chunks.pkl")
            if os.path.exists(chunks_path):
                with open(chunks_path, "rb") as f:
                    data = pickle.load(f)
                self.chunks = data.get("chunks", [])
                self.bm25 = data.get("bm25", None)
                print(f"✅ Chunks loaded - {len(self.chunks)} chunks")
                if self.bm25:
                    print("✅ BM25 index loaded")
                else:
                    print("⚠️ BM25 index tidak ditemukan, akan menggunakan keyword search")

            self.is_ready = True
            print("🚀 AI Engine siap!")
        except Exception as e:
            print(f"❌ Error loading: {str(e)}")
            self.is_ready = False

    def search_with_model(self, user_message: str, top_k: int = 10) -> list:
        """
        Gunakan BM25 model untuk mencari chunks yang relevan berdasarkan query user.
        Return list of unique filenames dari chunks yang ditemukan.
        """
        if not self.chunks:
            return []
        
        query_tokens = user_message.lower().split()
        
        if self.bm25:
            scores = self.bm25.get_scores(query_tokens)
            top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
            found_files = []
            for idx in top_indices:
                if scores[idx] > 0:
                    chunk = self.chunks[idx]
                    fname = chunk.get("file_name", "")
                    if fname and fname not in found_files:
                        found_files.append(fname)
            return found_files[:5]
        else:
            return self._fallback_keyword_search(user_message)

    def _fallback_keyword_search(self, user_message: str) -> list:
        """Fallback jika BM25 tidak tersedia"""
        user_message = user_message.lower()
        keywords = user_message.replace("cari", "").replace("tentang", "").replace("dokumen", "").split()
        keywords = [k.strip() for k in keywords if len(k) > 2]
        
        found_files = []
        for chunk in self.chunks:
            chunk_text = chunk.get("clean", "").lower()
            fname = chunk.get("file_name", "")
            for keyword in keywords:
                if keyword in chunk_text and fname not in found_files:
                    found_files.append(fname)
                    break
        
        return found_files[:5]

    def check_file_exists_in_gdrive(self, model_output_filename: str) -> bool:
        """
        Cek apakah filename yang di-output oleh model ada di daftar file GDrive.
        """
        return model_output_filename in self.file_names

    def get_gdrive_link(self, filename: str):
        """
        Mengambil link GDrive berdasarkan nama file.
        Hanya return link jika file ada di daftar GDrive.
        """
        if not self.check_file_exists_in_gdrive(filename):
            return None, None
        
        import hashlib
        encoded_name = filename.replace(" ", "+")
        search_url = f"https://drive.google.com/drive/folders/{GDRIVE_FOLDER_ID}?q={encoded_name}"
        file_id = hashlib.md5(filename.encode()).hexdigest()[:12]
        
        return file_id, search_url

    def process_query(self, user_message: str):
        """
        Main logic dengan flow yang benar:
        1. Input user -> AI Model (BM25 search)
        2. Model output -> daftar nama file yang relevan
        3. Cek apakah file-file tersebut ada di GDrive
        4. Return hasil
        """
        if not self.is_ready:
            return {"error": "AI not ready"}

        model_output_filenames = self.search_with_model(user_message)

        if not model_output_filenames:
            return {
                "found": False,
                "reply": "Maaf, model AI tidak menemukan dokumen yang relevan dengan pertanyaan Anda."
            }

        verified_files = []
        for fname in model_output_filenames:
            if self.check_file_exists_in_gdrive(fname):
                file_id, gdrive_link = self.get_gdrive_link(fname)
                if file_id:
                    verified_files.append({
                        "filename": fname,
                        "gdrive_id": file_id,
                        "gdrive_url": gdrive_link
                    })

        if not verified_files:
            return {
                "found": False,
                "reply": f"Model menyarankan {model_output_filenames}, tetapi file-file tersebut tidak ditemukan di Google Drive."
            }

        file_count = len(verified_files)
        if file_count == 1:
            reply = f"Saya menemukan 1 dokumen yang cocok: {verified_files[0]['filename']}"
        else:
            file_list_str = ", ".join([r['filename'] for r in verified_files[:3]])
            if file_count > 3:
                reply = f"Saya menemukan {file_count} dokumen yang cocok, termasuk: {file_list_str}, dan lainnya."
            else:
                reply = f"Saya menemukan {file_count} dokumen yang cocok: {file_list_str}"
        
        return {
            "found": True,
            "files": verified_files,
            "gdrive_folder": f"https://drive.google.com/drive/folders/{GDRIVE_FOLDER_ID}",
            "reply": reply
        }

ai_bot = AIEngine()
