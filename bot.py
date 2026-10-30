import asyncio
from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN
from modules import general, activations, otp, emails, info, callbacks # Tambahkan callbacks

async def main():
    client = TelegramClient('herosms_session', API_ID, API_HASH)

    # Daftarkan semua handlers
    general.register(client)
    activations.register(client)
    otp.register(client)
    emails.register(client)
    info.register(client)
    callbacks.register(client) # Registrasi modul callback (tombol inline)

    await client.start(bot_token=BOT_TOKEN)
    print("🤖 Bot HeroSMS Interaktif (Private) berjalan...")
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
