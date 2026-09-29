# Botv2-telegram
Bot with Button feature  2020

Berikut adalah kode lengkap untuk UBOT LIST yang bisa dijalankan di Termux dan di-upload ke GitHub. Saya buatkan beberapa file sekaligus.

## 📁 Struktur Project

```
ubot-list/
├── config.py
├── ubot_list.py
├── requirements.txt
├── README.md
└── start.sh
```

---

## 1️⃣ `config.py`

```python
# ═══════════════════════════════════════════
# KONFIGURASI UBOT LIST
# ═══════════════════════════════════════════

# Dapatkan API_ID & API_HASH di https://my.telegram.org
API_ID = 123456                    # Ganti dengan API ID kamu
API_HASH = "your_api_hash_here"   # Ganti dengan API HASH kamu

# ID Telegram kamu (admin). Bisa lebih dari 1.
# Cek ID di @userinfobot
ADMIN_IDS = [
    123456789,    # Ganti dengan ID Telegram kamu
    # 987654321,  # Tambah admin lain jika perlu
]

# Nama session file (akan dibuat otomatis)
SESSION_NAME = "ubot_list"

# File penyimpanan data
DATA_FILE = "ubot_data.json"
```

---

## 🚀 Cara Upload ke GitHub

```bash
# Di Termux:
git init
git add .
git commit -m "Initial commit - UBOT LIST"
git branch -M main
git remote add origin https://github.com/USERNAME/ubot-list.git
git push -u origin main
```

---

## ⚠️ Penting Sebelum Run

1. **Edit `config.py`** terlebih dahulu:
   - Dapatkan `API_ID` & `API_HASH` dari https://my.telegram.org/apps
   - Isi `ADMIN_IDS` dengan ID Telegram kamu

2. **Jangan upload file `ubot_list.session`** ke GitHub (sudah otomatis diabaikan jika pakai `.gitignore`)

3. **Tambahkan `.gitignore`**:
```bash
echo "ubot_list.session" >> .gitignore
echo "ubot_data.json" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.session-journal" >> .gitignore
```
