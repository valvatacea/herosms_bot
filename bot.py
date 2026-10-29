from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN
from modules import general, activations, otp, emails, info

client = TelegramClient('herosms_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Mendaftarkan semua handlers dari folder modules
general.register(client)
activations.register(client)
otp.register(client)
emails.register(client)
info.register(client)

if __name__ == '__main__':
    print("🤖 Bot HeroSMS Modular sedang berjalan...")
    client.run_until_disconnected()
