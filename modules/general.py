from telethon import events, Button
from hero_api import api
from utils import is_allowed, build_service_keyboard

def register(client):
    @client.on(events.NewMessage(pattern='(?i)^/start$', func=is_allowed))
    async def start(event):
        buttons = [
            [Button.inline("💳 Cek Saldo", b"menu_balance"), Button.inline("📋 Aktivasi Aktif", b"menu_active")],
            [Button.inline("🕒 Riwayat Terakhir", b"menu_history")],
            [Button.inline("🛒 Beli Nomor", b"menu_buy_start")] # Diubah agar langsung ke proses beli
        ]
        text = (
            "🤖 **HeroSMS Bot Interaktif**\n\n"
            "Selamat datang! Akun Anda telah diotorisasi.\n"
            "Silakan pilih menu di bawah ini:"
        )
        await event.reply(text, buttons=buttons)

    @client.on(events.NewMessage(pattern='(?i)^/balance$', func=is_allowed))
    async def balance(event):
        res = await api.request_stub("getBalance")
        if "ACCESS_BALANCE" in res:
            await event.reply(f"💳 **Saldo:** ${res.split(':')[1]}")
        else:
            await event.reply(f"⚠️ Error: `{res}`")
