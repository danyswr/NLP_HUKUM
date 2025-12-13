import gdown
import os

# Link GDrive yang kamu berikan
url = "https://drive.google.com/drive/folders/1yPc4Dyr0eM45NqNHCTDsiH2olOLyNqZQ?usp=sharing"

# Lokasi simpan (Current Directory)
output_path = "./" 

print(f"Memulai download folder dari GDrive...")

# Fungsi download_folder otomatis menangani rekursif folder
# quiet=False -> agar progress bar terlihat
# use_cookies=False -> biasanya aman untuk public folder
files = gdown.download_folder(url, output=output_path, quiet=False, use_cookies=False)

if files:
    print(f"\nBerhasil mendownload {len(files)} file/folder.")
    print(f"Disimpan di: {os.path.abspath(output_path)}")
else:
    print("\nGagal mendownload atau folder kosong.")

    