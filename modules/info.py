from telethon import events
from hero_api import api

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^/offers\s+([a-zA-Z]+)\s+(\d+)$', func=is_allowed))
    async def offers(event):
        service, country = event.pattern_match.groups()
        status, res = await api.request_v1('GET', f'/activations/offers/sms?services={service.lower()}&countries={country}')
        
        if status == 200:
            try:
                offer = res["data"][service.lower()][country]
                price = offer["prices"]["default"]
                stock = offer["counts"]["total"]
                await event.reply(f"📊 **Penawaran SMS:**\nLayanan: `{service}`\nNegara: `{country}`\n💰 Harga: `${price}`\n📦 Stok: `{stock}`")
            except KeyError:
                await event.reply("⚠️ Tidak ada stok untuk parameter tersebut.")
        else:
            await event.reply("❌ Gagal mengambil penawaran.")

    @client.on(events.NewMessage(pattern='(?i)^/countries$'))
    async def countries(event):
        await event.reply("Untuk melihat daftar kode negara HeroSMS secara lengkap, silakan kunjungi:\n`https://hero-sms.com/stubs/handler_api.php?action=getCountries`")
        
    @client.on(events.NewMessage(pattern='(?i)^/services$'))
    async def services(event):
        await event.reply("Untuk melihat daftar kode layanan HeroSMS secara lengkap, silakan kunjungi:\n`https://hero-sms.com/stubs/handler_api.php?action=getServicesList`")
