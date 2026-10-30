from telethon import events
from hero_api import api
from utils import is_allowed

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^/email_buy\s+([a-zA-Z0-9.-]+)\s+([a-zA-Z0-9.-]+)$', func=is_allowed))
    async def email_buy(event):
        site, domain = event.pattern_match.groups()
        status, res = await api.request_v1('POST', '/emails', json={"site": site.lower(), "domain": domain.lower()})
        if status == 201 and "data" in res:
            data = res["data"]
            await event.reply(f"✅ **Email Dibeli!**\n🆔 ID: `{data['id']}`\n📧 Email: `{data['email']}`\n💰 Harga: ${data['cost']}")
        else:
            await event.reply(f"❌ Gagal membeli email.")

    @client.on(events.NewMessage(pattern=r'(?i)^/email_status\s+(\d+)$'))
    async def email_status(event):
        email_id = event.pattern_match.group(1)
        status, res = await api.request_v1('GET', f'/emails/{email_id}')
        if status == 200 and "data" in res:
            d = res["data"]
            code = d.get('value', 'Belum ada')
            await event.reply(f"📧 **Status (ID {email_id})**\nStatus: `{d['status']}`\n🔑 Kode: `{code}`")
        else:
            await event.reply("❌ Email tidak ditemukan.")

    @client.on(events.NewMessage(pattern=r'(?i)^/email_cancel\s+(\d+)$'))
    async def email_cancel(event):
        email_id = event.pattern_match.group(1)
        status, _ = await api.request_v1('DELETE', f'/emails/{email_id}')
        await event.reply("✅ Pesanan email dibatalkan." if status == 204 else "❌ Gagal membatalkan.")
        
    @client.on(events.NewMessage(pattern=r'(?i)^/email_offers\s+([a-zA-Z0-9.-]+)$'))
    async def email_offers(event):
        site = event.pattern_match.group(1)
        status, res = await api.request_v1('GET', f'/emails/offers?site={site}')
        if status == 200 and res.get("data"):
            d = res["data"][0] # Ambil domain pertama
            domain, cost = d['domain'], d['offers'][0]['cost']
            await event.reply(f"📊 **Penawaran {site}:**\nDomain: `{domain}`\nHarga Mulai: `${cost}`")
        else:
            await event.reply("⚠️ Tidak ada penawaran tersedia.")
