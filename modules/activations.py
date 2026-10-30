from telethon import events
from hero_api import api
from utils import is_allowed, build_service_keyboard

def register(client):
    # Perintah /buy kini memunculkan daftar aplikasi interaktif
    @client.on(events.NewMessage(pattern=r'(?i)^/buy$', func=is_allowed))
    async def buy_start(event):
        msg = await event.reply("🔄 Memuat daftar aplikasi/layanan...")
        
        services = await api.get_all_services()
        if not services:
            return await msg.edit("⚠️ Gagal memuat daftar layanan dari server.")
            
        buttons = build_service_keyboard(services, page=0)
        await msg.edit("🛒 **Pilih Aplikasi / Layanan**\n\nSilakan pilih aplikasi yang ingin diregistrasi (Hal 1):", buttons=buttons)

    # (Biarkan handler /active, /history, /cancel, /finish dll tetap seperti sebelumnya)
