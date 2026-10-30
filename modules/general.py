from telethon import events, Button
from hero_api import api
from utils import is_allowed

def register(client):
    @client.on(events.NewMessage(pattern='(?i)^/start$', func=is_allowed))
    async def start(event):
        # Membuat tombol menu interaktif
        buttons = [
            [Button.inline("💳 Cek Saldo", b"menu_balance"), Button.inline("📋 Aktivasi Aktif", b"menu_active")],
            [Button.inline("🕒 Riwayat Terakhir", b"menu_history")],
            [Button.inline("🛒 Cara Beli Nomor", b"menu_help_buy")]
        ]
        text = (
            "🤖 **HeroSMS Bot Interaktif**\n\n"
            "Selamat datang! Akun Anda telah diotorisasi.\n"
            "Silakan pilih menu di bawah ini:"
        )
        await event.reply(text, buttons=buttons)
