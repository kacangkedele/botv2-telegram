# Botv2-telegram

UBOT LIST — Versi yang disesuaikan untuk menggunakan Telegram Bot (BOT_TOKEN) dan perintah dengan slash (/).

> Perubahan utama pada repository ini:
> - Beralih dari login Telethon (API_ID/API_HASH) ke Telegram Bot Token (BOT_TOKEN).
> - Menggunakan library `python-telegram-bot` untuk polling bot.
> - Perintah kini menggunakan slash (contoh: `/menu`) — alias dot (`.menu`) tetap didukung.
> - File utama: `ubotlist.py` (jalankan dengan `python ubotlist.py`).

## 📁 Struktur Project

```
botv2-telegram/
├── config.py        # Isi BOT_TOKEN dan ADMIN_IDS
├── ubotlist.py      # Script utama (python-telegram-bot)
├── requirements.txt # dependency
├── README.md
└── start.sh
```

---

## 🔧 Konfigurasi (config.py)

Buka `config.py` lalu isi token BotFather dan ID admin.

Contoh isi `config.py`:

```python
BOT_TOKEN = "123456789:ABCDEFghijklmnopQRSTUVwxYZ"  # Ganti dengan token BotFather

ADMIN_IDS = [
    123456789,  # Ganti dengan ID Telegram admin
]

DATA_FILE = "ubot_data.json"
```

Catatan:
- Jangan publikasikan BOT_TOKEN Anda.
- Gunakan ID admin (integer) — dapat diambil dari @userinfobot.

---

## ✅ Perintah yang didukung

- /menu — buka menu tombol
- /on — aktifkan bot di chat
- /off — matikan bot di chat
- /list — lihat daftar taruhan ronde ini
- /rs — reset list (mulai ronde baru)
- /rk — rekap total
- /perak — set mode perak (kali 1000)
- /nonperak — set mode normal
- /cmd atau /help — panduan lengkap

Alias legacy (masih didukung):
- .menu, .on, .off, .list, .rs, .rk, .perak, .nonperak, .cmd

Cara memasang taruhan di chat (ketika bot aktif):
- K5, B10, 5K, 10B (format fleksibel, spasi atau tanpa)

---

## 📦 Instalasi

Pastikan Python 3.9+ terpasang, lalu install dependency:

```bash
pip install -r requirements.txt
```

---

## ▶️ Menjalankan Bot

1. Edit `config.py` dan masukkan `BOT_TOKEN` serta `ADMIN_IDS`.
2. Jalankan:

```bash
python ubotlist.py
```

Bot akan berjalan menggunakan polling. Di grup, gunakan `/menu` untuk membuka tombol.

---

## ℹ️ Catatan Tambahan

- Data taruhan disimpan di `ubot_data.json`.
- Jangan commit atau unggah file yang berisi token.
- Jika ingin fitur tambahan (contoh: /start, backup otomatis, multi-group logging), beri tahu saya untuk saya tambahkan.

---

Terima kasih — selamat mencoba! Jika ingin saya perapikan README lagi (terjemahan, tambahan screenshot, contoh konfigurasi environment), saya bantu lanjutkan.