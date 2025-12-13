import os
import json
import pickle
import warnings
import csv
import sys
from rank_bm25 import BM25Okapi

csv.field_size_limit(sys.maxsize)
warnings.filterwarnings("ignore")

ASSETS_DIR = "models-asset"
GDRIVE_FOLDER_ID = "1vYRLxyfqQSV_tJmTcXx423I5AacxFJOQ"

class AIEngine:
    def __init__(self):
        self.bm25 = None
        self.chunks = None
        self.file_names = []
        self.documents = {}
        self.doc_tokens = []
        self.doc_filenames = []
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
                    print("✅ BM25 index loaded from pickle")

            dataset_path = os.path.join(ASSETS_DIR, "dataset_bpk.csv")
            if os.path.exists(dataset_path):
                self._load_dataset_for_search(dataset_path)

            if not self.bm25 and self.chunks:
                self._build_bm25_from_chunks()

            self.is_ready = True
            print("🚀 AI Engine siap!")
        except Exception as e:
            print(f"❌ Error loading: {str(e)}")
            import traceback
            traceback.print_exc()
            self.is_ready = False

    def _load_dataset_for_search(self, dataset_path: str):
        """Load dataset CSV for better search capability"""
        print(f"📂 Loading dataset dari {dataset_path}...")
        try:
            with open(dataset_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    filename = row.get('Nama File', '').strip()
                    content = row.get('Isi Teks Dokumen', '').strip()
                    if filename and content:
                        if filename not in self.documents:
                            self.documents[filename] = content[:10000]
                        else:
                            self.documents[filename] += " " + content[:5000]
            
            print(f"✅ Dataset loaded - {len(self.documents)} dokumen unik")
            
            if self.documents:
                self._build_bm25_from_documents()
        except Exception as e:
            print(f"⚠️ Error loading dataset: {str(e)}")

    def _build_bm25_from_documents(self):
        """Build BM25 index from documents"""
        print("🔄 Building BM25 index dari documents...")
        self.doc_tokens = []
        self.doc_filenames = []
        
        for filename, content in self.documents.items():
            tokens = self._tokenize(content)
            if tokens:
                self.doc_tokens.append(tokens)
                self.doc_filenames.append(filename)
        
        if self.doc_tokens:
            self.bm25 = BM25Okapi(self.doc_tokens)
            print(f"✅ BM25 index built - {len(self.doc_filenames)} dokumen")

    def _build_bm25_from_chunks(self):
        """Build BM25 from chunks if no other index available"""
        print("🔄 Building BM25 index dari chunks...")
        tokenized_chunks = []
        for chunk in self.chunks:
            text = chunk.get("clean", chunk.get("text", ""))
            tokens = self._tokenize(text)
            if tokens:
                tokenized_chunks.append(tokens)
        
        if tokenized_chunks:
            self.bm25 = BM25Okapi(tokenized_chunks)
            print(f"✅ BM25 index built dari {len(tokenized_chunks)} chunks")

    def _tokenize(self, text: str) -> list:
        """Simple tokenization"""
        text = text.lower()
        stopwords = {'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'dengan', 'adalah', 
                     'pada', 'ini', 'itu', 'atau', 'dalam', 'tidak', 'juga', 'akan',
                     'oleh', 'sebagai', 'tersebut', 'dapat', 'telah', 'bahwa', 'tentang',
                     'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been'}
        tokens = text.split()
        tokens = [t.strip('.,;:!?()[]{}"\'-') for t in tokens]
        tokens = [t for t in tokens if len(t) > 2 and t not in stopwords]
        return tokens

    def search_with_model(self, user_message: str, top_k: int = 20) -> list:
        """
        Gunakan BM25 model untuk mencari dokumen yang relevan.
        Return list of unique filenames dari hasil pencarian.
        """
        if not self.bm25:
            print("⚠️ BM25 tidak tersedia, menggunakan keyword search")
            return self._fallback_keyword_search(user_message)
        
        query_tokens = self._tokenize(user_message)
        if not query_tokens:
            return []
        
        print(f"🔍 Searching with tokens: {query_tokens[:10]}")
        
        scores = self.bm25.get_scores(query_tokens)
        
        if self.doc_filenames:
            scored_docs = list(zip(self.doc_filenames, scores))
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            
            found_files = []
            for filename, score in scored_docs[:top_k]:
                if score > 0 and filename not in found_files:
                    found_files.append(filename)
                    print(f"  📄 {filename}: score={score:.2f}")
            
            return found_files[:10]
        elif self.chunks:
            top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
            found_files = []
            for idx in top_indices:
                if scores[idx] > 0:
                    chunk = self.chunks[idx]
                    fname = chunk.get("file_name", "")
                    if fname and fname not in found_files:
                        found_files.append(fname)
                        print(f"  📄 {fname}: score={scores[idx]:.2f}")
            return found_files[:10]
        
        return []

    def _fallback_keyword_search(self, user_message: str) -> list:
        """Fallback jika BM25 tidak tersedia"""
        keywords = self._tokenize(user_message)
        found_files = []
        
        for filename in self.file_names:
            filename_lower = filename.lower()
            for keyword in keywords:
                if keyword in filename_lower:
                    if filename not in found_files:
                        found_files.append(filename)
                    break
        
        if self.documents:
            for filename, content in self.documents.items():
                content_lower = content.lower()
                match_count = sum(1 for kw in keywords if kw in content_lower)
                if match_count >= 2 and filename not in found_files:
                    found_files.append(filename)
        
        return found_files[:10]

    def check_file_exists_in_gdrive(self, model_output_filename: str) -> bool:
        """Cek apakah filename ada di daftar file GDrive."""
        return model_output_filename in self.file_names

    def get_document_preview(self, filename: str, max_length: int = 500) -> str:
        """Get preview content of a document"""
        if filename in self.documents:
            content = self.documents[filename]
            if len(content) > max_length:
                return content[:max_length] + "..."
            return content
        
        for chunk in (self.chunks or []):
            if chunk.get("file_name") == filename:
                text = chunk.get("text", "")[:max_length]
                return text + "..." if len(chunk.get("text", "")) > max_length else text
        
        return "Preview tidak tersedia"

    def get_gdrive_link(self, filename: str):
        """Mengambil link GDrive berdasarkan nama file."""
        if not self.check_file_exists_in_gdrive(filename):
            return None, None
        
        import hashlib
        encoded_name = filename.replace(" ", "+")
        search_url = f"https://drive.google.com/drive/folders/{GDRIVE_FOLDER_ID}?q={encoded_name}"
        file_id = hashlib.md5(filename.encode()).hexdigest()[:12]
        
        return file_id, search_url

    def process_query(self, user_message: str):
        """
        Main logic:
        1. Input user -> AI Model (BM25 search)
        2. Model output -> daftar nama file yang relevan
        3. Cek apakah file ada di GDrive
        4. Return hasil dengan preview
        """
        if not self.is_ready:
            return {"error": "AI not ready"}

        print(f"\n📝 Processing query: {user_message}")
        
        model_output_filenames = self.search_with_model(user_message)

        if not model_output_filenames:
            return {
                "found": False,
                "reply": "Maaf, model AI tidak menemukan dokumen yang relevan dengan pertanyaan Anda. Coba gunakan kata kunci yang lebih spesifik seperti 'UU', 'peraturan', atau nomor undang-undang."
            }

        verified_files = []
        for fname in model_output_filenames:
            if self.check_file_exists_in_gdrive(fname):
                file_id, gdrive_link = self.get_gdrive_link(fname)
                if file_id:
                    preview = self.get_document_preview(fname)
                    verified_files.append({
                        "filename": fname,
                        "gdrive_id": file_id,
                        "gdrive_url": gdrive_link,
                        "preview": preview
                    })

        if not verified_files:
            return {
                "found": False,
                "reply": f"Model menemukan {len(model_output_filenames)} dokumen relevan, tetapi tidak ditemukan di Google Drive. File yang dicari: {', '.join(model_output_filenames[:3])}"
            }

        file_count = len(verified_files)
        if file_count == 1:
            reply = f"Saya menemukan 1 dokumen yang cocok: {verified_files[0]['filename']}"
        else:
            file_list_str = ", ".join([r['filename'] for r in verified_files[:3]])
            if file_count > 3:
                reply = f"Saya menemukan {file_count} dokumen yang cocok, termasuk: {file_list_str}, dan {file_count - 3} lainnya."
            else:
                reply = f"Saya menemukan {file_count} dokumen yang cocok: {file_list_str}"
        
        return {
            "found": True,
            "files": verified_files,
            "gdrive_folder": f"https://drive.google.com/drive/folders/{GDRIVE_FOLDER_ID}",
            "reply": reply
        }

ai_bot = AIEngine()
