from telethon import events
from hero_api import api

def register(client):
    @client.on(events.NewMessage(pattern='(?i)^/start$'))
    async def start(event):
        text = (
            "🤖 **HeroSMS Full API Bot**\n\n"
            "**Layanan SMS:**\n"
            "`/balance` - Cek Saldo\n"
            "`/buy <layanan> <negara>` - Beli Nomor\n"
            "`/active` | `/history` - Daftar/Riwayat Aktivasi\n"
            "`/cancel <id>` | `/finish <id>` - Batal/Selesai\n"
            "`/replace <id>` - Ganti Nomor (Replace)\n"
            "`/reactivate <id>` - Aktifkan ulang nomor lama\n"
            "`/prolong <id> <jam>` - Perpanjang masa aktif (Sewa)\n\n"
            "**OTP & Info:**\n"
            "`/sms <id>` | `/sms_all <id>` - Cek OTP\n"
            "`/offers <layanan> <negara>` - Harga & Stok\n"
            "`/countries` | `/services` - List Kode\n\n"
            "**Email Aktivasi:**\n"
            "`/email_buy <situs> <domain>`\n"
            "`/email_status <id>`\n"
            "`/email_cancel <id>`\n"
            "`/email_offers <situs>`"
        )
        await event.reply(text)

    @client.on(events.NewMessage(pattern='(?i)^/balance$'))
    async def balance(event):
        res = await api.request_stub("getBalance")
        if "ACCESS_BALANCE" in res:
            await event.reply(f"💳 **Saldo:** ${res.split(':')[1]}")
        else:
            await event.reply(f"⚠️ Error: `{res}`")
