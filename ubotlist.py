"""
╔══════════════════════════════════════════════════╗
║        UBOT LIST - Manajemen Taruhan K/B         ║
║          With Beautiful Button Interface         ║
║             By Angga Official                    ║
╚══════════════════════════════════════════════════╝
"""

import os
import re
import json
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButton, ReplyInlineMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, ADMIN_IDS, SESSION_NAME, DATA_FILE

# ═══════════════════════════════════════════
# FIX PYTHON 3.14: Buat event loop manual
# ═══════════════════════════════════════════
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


# ═══════════════════════════════════════════
# STORAGE - Load & Save JSON
# ═══════════════════════════════════════════

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "active": {},
        "perak_mode": {},
        "bets": {},
        "aliases": {},
        "geseran": {},
    }

def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        print(f"[ERROR] Gagal save data: {e}")

data = load_data()

# ═══════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════

def is_admin(user_id):
    return user_id in ADMIN_IDS

def is_active(chat_id):
    return data["active"].get(str(chat_id), False)

def is_perak(chat_id):
    return data["perak_mode"].get(str(chat_id), True)

def get_bets(chat_id):
    cid = str(chat_id)
    if cid not in data["bets"]:
        data["bets"][cid] = {}
    return data["bets"][cid]

def get_geseran(chat_id):
    cid = str(chat_id)
    if cid not in data["geseran"]:
        data["geseran"][cid] = {}
    return data["geseran"][cid]

def parse_bet(text):
    text = text.strip().upper().replace(",", ".")
    m = re.match(r"^([KB])\s*(\d+(?:\.\d+)?)$", text)
    if m:
        return m.group(1), float(m.group(2))
    m = re.match(r"^(\d+(?:\.\d+)?)\s*([KB])$", text)
    if m:
        return m.group(2), float(m.group(1))
    return None, None

def calc_amount(raw, perak_mode):
    if perak_mode:
        return int(raw * 1000)
    if raw == int(raw):
        return int(raw)
    return raw

def format_amount(amount):
    if isinstance(amount, int):
        return f"{amount:,}".replace(",", ".")
    return str(amount)

async def get_display_name(user):
    if not user:
        return "Unknown"
    name = user.first_name or ""
    if user.last_name:
        name += f" {user.last_name}"
    return name.strip() or f"User_{user.id}"

def create_main_menu():
    """Buat tombol menu utama"""
    buttons = [
        [InlineKeyboardButton("✅ ON Bot", callback_data="cmd_on"),
         InlineKeyboardButton("❌ OFF Bot", callback_data="cmd_off")],
        [InlineKeyboardButton("📋 LIST", callback_data="cmd_list"),
         InlineKeyboardButton("🗑 RESET", callback_data="cmd_rs")],
        [InlineKeyboardButton("📊 REKAP", callback_data="cmd_rk"),
         InlineKeyboardButton("💰 PERAK", callback_data="cmd_perak")],
        [InlineKeyboardButton("💵 NON-PERAK", callback_data="cmd_nonperak")],
        [InlineKeyboardButton("📖 BANTUAN", callback_data="cmd_help")],
    ]
    return InlineKeyboardMarkup(buttons)

def create_list_menu():
    """Buat tombol untuk list"""
    buttons = [
        [InlineKeyboardButton("🔄 REFRESH", callback_data="cmd_list"),
         InlineKeyboardButton("📊 REKAP", callback_data="cmd_rk")],
        [InlineKeyboardButton("🗑 RESET LIST", callback_data="cmd_rs")],
        [InlineKeyboardButton("⬅️ KEMBALI", callback_data="cmd_menu")],
    ]
    return InlineKeyboardMarkup(buttons)

def create_help_menu():
    """Buat tombol untuk bantuan"""
    buttons = [
        [InlineKeyboardButton("⬅️ KEMBALI", callback_data="cmd_menu")],
    ]
    return InlineKeyboardMarkup(buttons)

# ═══════════════════════════════════════════
# INISIALISASI CLIENT
# ═══════════════════════════════════════════

client = TelegramClient(SESSION_NAME, API_ID, API_HASH, loop=loop)


# ═══════════════════════════════════════════
# CALLBACK HANDLERS
# ═══════════════════════════════════════════

@client.on(events.CallbackQuery())
async def handle_callback(event):
    data_query = event.data.decode('utf-8')
    
    if data_query == "cmd_menu":
        await handle_menu(event)
    elif data_query == "cmd_on":
        await handle_on(event)
    elif data_query == "cmd_off":
        await handle_off(event)
    elif data_query == "cmd_list":
        await handle_list(event)
    elif data_query == "cmd_rs":
        await handle_rs(event)
    elif data_query == "cmd_rk":
        await handle_rk(event)
    elif data_query == "cmd_perak":
        await handle_perak(event)
    elif data_query == "cmd_nonperak":
        await handle_nonperak(event)
    elif data_query == "cmd_help":
        await handle_help(event)

async def handle_menu(event):
    if not is_admin(event.sender_id):
        await event.answer("❌ Anda bukan admin!", alert=True)
        return
    msg = """╔════════════════════════════════════╗
║  🤖 UBOT LIST - MENU UTAMA 🤖      ║
║                                    ║
║  Selamat datang di UBOT LIST!     ║
║  Gunakan tombol di bawah untuk    ║
║  mengelola taruhan K/B 💰         ║
╚════════════════════════════════════╝

Pilih aksi yang ingin dilakukan:"""
    await event.edit(msg, buttons=create_main_menu())
    await event.answer()

async def handle_on(event):
    if not is_admin(event.sender_id):
        await event.answer("❌ Anda bukan admin!", alert=True)
        return
    cid = str(event.chat_id)
    data["active"][cid] = True
    if cid not in data["perak_mode"]:
        data["perak_mode"][cid] = True
    save_data()
    msg = """╔════════════════════════════════════╗
║  ✅ UBOT LIST AKTIF ✅              ║
╚════════════════════════════════════╝

🎯 Bot mulai mencatat bet!
🔄 Mode: PERAK (B1 = 1000)

Silakan mulai pasang bet di grup.
📝 Format: K5, B10, atau 5K, 10B

Ketik .cmd untuk bantuan lengkap."""
    await event.edit(msg, buttons=create_main_menu())
    await event.answer("✅ Bot berhasil diaktifkan!")

async def handle_off(event):
    if not is_admin(event.sender_id):
        await event.answer("❌ Anda bukan admin!", alert=True)
        return
    cid = str(event.chat_id)
    data["active"][cid] = False
    save_data()
    msg = """╔════════════════════════════════════╗
║  ❌ UBOT LIST DIMATIKAN ❌          ║
╚════════════════════════════════════╝

🛑 Bot berhenti mencatat bet.

Untuk mengaktifkan kembali,
klik tombol ✅ ON Bot"""
    await event.edit(msg, buttons=create_main_menu())
    await event.answer("❌ Bot berhasil dimatikan!")

async def handle_list(event):
    bets = get_bets(event.chat_id)
    if not bets:
        msg = """╔════════════════════════════════════╗
║  📋 LIST RONDE INI 📋              ║
╚════════════════════════════════════╝

❌ List masih kosong!
Belum ada yang pasang bet.

Tunggu atau minta member untuk
pasang bet terlebih dahulu. 💰"""
    else:
        k_list, b_list = [], []
        for uid, info in bets.items():
            line = f"• {info['name']} {format_amount(info['amount'])}"
            if info["username"]:
                line += f" {info['username']}"
            if info["type"] == "K":
                k_list.append(line)
            else:
                b_list.append(line)

        k_total = sum(i["amount"] for i in bets.values() if i["type"] == "K")
        b_total = sum(i["amount"] for i in bets.values() if i["type"] == "B")

        msg = "╔════════════════════════════════════╗\n"
        msg += "║  📋 LIST RONDE INI 📋              ║\n"
        msg += "╚════════════════════════════════════╝\n\n"
        
        if k_list:
            msg += "🔻 **KECIL (K)**\n"
            msg += "\n".join(k_list) + "\n\n"
        else:
            msg += "🔻 KECIL: - (kosong)\n\n"
        
        if b_list:
            msg += "🔺 **BESAR (B)**\n"
            msg += "\n".join(b_list) + "\n\n"
        else:
            msg += "🔺 BESAR: - (kosong)\n\n"
        
        msg += "═══════════════════════════════════\n"
        msg += f"💰 Total K: **{format_amount(k_total)}**\n"
        msg += f"💰 Total B: **{format_amount(b_total)}**\n"
        msg += f"👥 Pemain: **{len(bets)}** orang\n"
        msg += "═══════════════════════════════════"

    await event.edit(msg, buttons=create_list_menu())
    await event.answer()

async def handle_rs(event):
    if not is_admin(event.sender_id):
        await event.answer("❌ Anda bukan admin!", alert=True)
        return
    cid = str(event.chat_id)
    data["bets"][cid] = {}
    save_data()
    msg = """╔════════════════════════════════════╗
║  🗑 RESET LIST - RONDE BARU 🗑      ║
╚════════════════════════════════════╝

✅ List berhasil dikosongkan!

🎯 Ronde baru dimulai.
Silakan mulai pasang bet lagi! 💰

📝 Format: K5, B10, atau 5K, 10B"""
    await event.edit(msg, buttons=create_main_menu())
    await event.answer("✅ List berhasil direset!")

async def handle_rk(event):
    bets = get_bets(event.chat_id)
    if not bets:
        msg = """╔════════════════════════════════════╗
║  📊 REKAP TOTAL 📊                  ║
╚════════════════════════════════════╝

❌ List kosong!
Tidak ada yang bisa direkap."""
    else:
        k_total = sum(i["amount"] for i in bets.values() if i["type"] == "K")
        b_total = sum(i["amount"] for i in bets.values() if i["type"] == "B")
        selisih = abs(k_total - b_total)
        k_count = sum(1 for i in bets.values() if i["type"] == "K")
        b_count = sum(1 for i in bets.values() if i["type"] == "B")

        msg = "╔════════════════════════════════════╗\n"
        msg += "║  📊 REKAP TOTAL 📊                  ║\n"
        msg += "╚════════════════════════════════════╝\n\n"
        msg += f"🔻 KECIL: {k_count} pemain → **{format_amount(k_total)}**\n"
        msg += f"🔺 BESAR: {b_count} pemain → **{format_amount(b_total)}**\n"
        msg += "═══════════════════════════════════\n\n"
        
        if k_total > b_total:
            msg += f"⚠️ **BESAR KURANG**\n"
            msg += f"💰 B perlu +**{format_amount(selisih)}**\n\n"
            msg += "📌 Tambahkan bet di pihak B!"
        elif b_total > k_total:
            msg += f"⚠️ **KECIL KURANG**\n"
            msg += f"💰 K perlu +**{format_amount(selisih)}**\n\n"
            msg += "📌 Tambahkan bet di pihak K!"
        else:
            msg += f"✅ **SEIMBANG!**\n"
            msg += f"🎯 K dan B sudah seimbang sempurna!"

    await event.edit(msg, buttons=create_list_menu())
    await event.answer()

async def handle_perak(event):
    if not is_admin(event.sender_id):
        await event.answer("❌ Anda bukan admin!", alert=True)
        return
    data["perak_mode"][str(event.chat_id)] = True
    save_data()
    msg = """╔════════════════════════════════════╗
║  💰 MODE PERAK AKTIF 💰              ║
╚════════════════════════════════════╝

🎯 Konversi taruhan:
B1  = 1.000
B10 = 10.000
B50 = 50.000

✅ Setiap bet akan dikali 1000"""
    await event.edit(msg, buttons=create_main_menu())
    await event.answer("✅ Mode PERAK diaktifkan!")

async def handle_nonperak(event):
    if not is_admin(event.sender_id):
        await event.answer("❌ Anda bukan admin!", alert=True)
        return
    data["perak_mode"][str(event.chat_id)] = False
    save_data()
    msg = """╔════════════════════════════════════╗
║  💵 MODE NON-PERAK AKTIF 💵          ║
╚════════════════════════════════════╝

🎯 Taruhan nilai asli:
B1  = 1
B10 = 10
B50 = 50

✅ Bet akan dihitung nilai aslinya"""
    await event.edit(msg, buttons=create_main_menu())
    await event.answer("✅ Mode NON-PERAK diaktifkan!")

async def handle_help(event):
    msg = """╔════════════════════════════════════╗
║  📖 PANDUAN LENGKAP 📖              ║
╚════════════════════════════════════╝

🔘 **TOMBOL UTAMA**
✅ ON Bot → Aktifkan bot
❌ OFF Bot → Matikan bot
📋 LIST → Lihat daftar bet
🗑 RESET → Kosongkan list
📊 REKAP → Lihat perhitungan
💰 PERAK → Mode x1000
💵 NON-PERAK → Mode normal

📝 **FORMAT BET**
K5 = Kecil 5
B10 = Besar 10
5K = Kecil 5 (dibalik)
10B = Besar 10 (dibalik)

⚙️ **COMMAND TEXT**
.on / .off = Aktif/Matikan
.list = Daftar bet
.rs = Reset
.rk = Rekap
.perak / .nonperak = Mode
.cmd = Bantuan

👨‍💼 Hanya admin yang bisa
gunakan command!"""
    await event.edit(msg, buttons=create_help_menu())
    await event.answer()

# ═══════════════════════════════════════════
# COMMAND: .menu (Buka menu tombol)
# ═══════════════════════════════════════════

@client.on(events.NewMessage(pattern=r"^[./]menu$"))
async def cmd_menu(event):
    if not is_admin(event.sender_id):
        return
    msg = """╔════════════════════════════════════╗
║  🤖 UBOT LIST - MENU UTAMA 🤖      ║
║                                    ║
║  Selamat datang di UBOT LIST!     ║
║  Gunakan tombol di bawah untuk    ║
║  mengelola taruhan K/B 💰         ║
╚════════════════════════════════════╝

Pilih aksi yang ingin dilakukan:"""
    await event.reply(msg, buttons=create_main_menu())

@client.on(events.NewMessage(pattern=r"^[./]on$"))
async def cmd_on_text(event):
    if not is_admin(event.sender_id):
        return
    cid = str(event.chat_id)
    data["active"][cid] = True
    if cid not in data["perak_mode"]:
        data["perak_mode"][cid] = True
    save_data()
    msg = """╔════════════════════════════════════╗
║  ✅ UBOT LIST AKTIF ✅              ║
╚════════════════════════════════════╝

🎯 Bot mulai mencatat bet!
🔄 Mode: PERAK (B1 = 1000)

Silakan mulai pasang bet di grup.
📝 Format: K5, B10, atau 5K, 10B

Ketik .cmd untuk bantuan lengkap."""
    await event.reply(msg, buttons=create_main_menu())

@client.on(events.NewMessage(pattern=r"^[./]off$"))
async def cmd_off_text(event):
    if not is_admin(event.sender_id):
        return
    cid = str(event.chat_id)
    data["active"][cid] = False
    save_data()
    msg = """╔════════════════════════════════════╗
║  ❌ UBOT LIST DIMATIKAN ❌          ║
╚════════════════════════════════════╝

🛑 Bot berhenti mencatat bet.

Untuk mengaktifkan kembali,
klik tombol ✅ ON Bot"""
    await event.reply(msg, buttons=create_main_menu())

@client.on(events.NewMessage(pattern=r"^[./]list$"))
async def cmd_list_text(event):
    bets = get_bets(event.chat_id)
    if not bets:
        msg = """╔════════════════════════════════════╗
║  📋 LIST RONDE INI 📋              ║
╚════════════════════════════════════╝

❌ List masih kosong!
Belum ada yang pasang bet."""
    else:
        k_list, b_list = [], []
        for uid, info in bets.items():
            line = f"• {info['name']} {format_amount(info['amount'])}"
            if info["username"]:
                line += f" {info['username']}"
            if info["type"] == "K":
                k_list.append(line)
            else:
                b_list.append(line)

        k_total = sum(i["amount"] for i in bets.values() if i["type"] == "K")
        b_total = sum(i["amount"] for i in bets.values() if i["type"] == "B")

        msg = "╔════════════════════════════════════╗\n"
        msg += "║  📋 LIST RONDE INI 📋              ║\n"
        msg += "╚════════════════════════════════════╝\n\n"
        msg += "🔻 **KECIL (K)**\n" if k_list else "🔻 KECIL: - (kosong)\n"
        msg += ("\n".join(k_list) + "\n\n") if k_list else ""
        msg += "🔺 **BESAR (B)**\n" if b_list else "🔺 BESAR: - (kosong)\n"
        msg += ("\n".join(b_list) + "\n\n") if b_list else ""
        msg += "═══════════════════════════════════\n"
        msg += f"💰 Total K: **{format_amount(k_total)}**\n"
        msg += f"💰 Total B: **{format_amount(b_total)}**\n"
        msg += f"👥 Pemain: **{len(bets)}** orang"

    await event.reply(msg, buttons=create_list_menu())

@client.on(events.NewMessage(pattern=r"^[./]rs$"))
async def cmd_rs_text(event):
    if not is_admin(event.sender_id):
        return
    cid = str(event.chat_id)
    data["bets"][cid] = {}
    save_data()
    msg = """╔════════════════════════════════════╗
║  🗑 RESET LIST - RONDE BARU 🗑      ║
╚════════════════════════════════════╝

✅ List berhasil dikosongkan!

🎯 Ronde baru dimulai.
Silakan mulai pasang bet lagi! 💰"""
    await event.reply(msg, buttons=create_main_menu())

@client.on(events.NewMessage(pattern=r"^[./]cmd$"))
async def cmd_help_text(event):
    msg = """╔════════════════════════════════════╗
║  📖 PANDUAN LENGKAP 📖              ║
╚════════════════════════════════════╝

🔘 **COMMAND UTAMA**
.on = Aktifkan bot
.off = Matikan bot
.list = Lihat daftar bet
.rs = Reset list
.rk = Rekap total
.perak = Mode x1000
.nonperak = Mode normal
.menu = Buka menu tombol

📝 **FORMAT BET**
K5 = Kecil 5
B10 = Besar 10
5K = Kecil 5 (dibalik)
10B = Besar 10 (dibalik)

👨‍💼 Hanya admin yang bisa
gunakan command!

🤖 Klik /menu untuk tombol utama"""
    await event.reply(msg, buttons=create_help_menu())

# ═══════════════════════════════════════════
# HANDLER: Pasang Bet (K5, B10, 5K, 10B)
# ═══════════════════════════════════════════

@client.on(events.NewMessage())
async def handle_bet(event):
    if not event.text or not is_active(event.chat_id):
        return
    text = event.text.strip()
    if text.startswith(".") or text.startswith("/"):
        return

    bet_type, raw = parse_bet(text)
    if bet_type is None:
        return

    amount = calc_amount(raw, is_perak(event.chat_id))
    try:
        user = await event.get_sender()
        name = await get_display_name(user)
    except Exception:
        name = f"User_{event.sender_id}"
        user = None
    
    uname = f"@{user.username}" if user and user.username else ""
    get_bets(event.chat_id)[str(event.sender_id)] = {
        "name": name,
        "username": uname,
        "type": bet_type,
        "amount": amount
    }
    save_data()
    display_raw = int(raw) if raw == int(raw) else raw
    
    emoji_type = "🔻" if bet_type == "K" else "🔺"
    msg = f"{emoji_type} **{name}** → {bet_type}{display_raw}"
    await event.reply(msg)

# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════

async def main():
    print("=" * 50)
    print("  🚀 UBOT LIST - STARTING...")
    print("=" * 50)
    await client.start()
    me = await client.get_me()
    print(f"\n  ✅ Login sebagai: {me.first_name}")
    if me.username:
        print(f"  📱 Username: @{me.username}")
    print(f"  🆔 ID: {me.id}")
    print(f"  👑 Admin IDs: {ADMIN_IDS}")
    print("\n  📋 Bot aktif & menunggu command...")
    print("  Ketik .menu atau /menu di grup untuk membuka menu tombol.")
    print("=" * 50)
    print("  Tekan Ctrl+C untuk berhenti.\n")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n\n👋 Bot dihentikan. Sampai jumpa!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
