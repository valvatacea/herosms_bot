import asyncio
from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN
from modules import general, activations, otp, emails, info

async def main():
    # Inisialisasi client di dalam async block agar event loop sudah tersedia
    client = TelegramClient('herosms_session', API_ID, API_HASH)

    # Daftarkan semua handlers
    general.register(client)
    activations.register(client)
    otp.register(client)
    emails.register(client)
    info.register(client)

    # Start bot
    await client.start(bot_token=BOT_TOKEN)
    print("🤖 Bot HeroSMS Modular sedang berjalan...")
    
    # Tahan agar bot terus berjalan
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Jalankan event loop dengan standar Python modern
    asyncio.run(main())
