from telethon import events, Button
from hero_api import api
from utils import is_allowed

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^/buy\s+([a-zA-Z]+)\s+(\d+)$', func=is_allowed))
    async def buy(event):
        service, country = event.pattern_match.groups()
        payload = {"service": service.lower(), "country": int(country), "amount": 1}
        msg = await event.reply("🔄 Memproses...")
        
        status, res = await api.request_v1('POST', '/activations', json=payload)
        if status == 200 and "data" in res:
            act = res["data"][0]
            act_id = act['id']
            
            # Tombol aksi langsung setelah sukses beli
            buttons = [
                [Button.inline("✉️ Cek SMS", f"sms_{act_id}".encode())],
                [Button.inline("✅ Selesai", f"fin_{act_id}".encode()), Button.inline("❌ Batal", f"can_{act_id}".encode())]
            ]
            
            text = f"✅ **Sukses Beli!**\n🆔 ID: `{act_id}`\n📱 Nomor: `+{act['phone']}`\n💰 Harga: ${act['price']}"
            await msg.edit(text, buttons=buttons)
        else:
            await msg.edit(f"❌ Gagal membeli (Code: {status})")

    @client.on(events.NewMessage(pattern='(?i)^/active$', func=is_allowed))
    async def active(event):
        status, res = await api.request_v1('GET', '/activations?size=10')
        if status == 200 and res.get("data"):
            await event.reply("📋 **Aktivasi Anda yang Sedang Berjalan:**")
            # Keluarkan 1 pesan + tombol untuk SETIAP nomor aktif
            for a in res["data"]:
                act_id = a['id']
                text = f"🆔 `{act_id}` | 📱 `+{a['phone']}` ({a['service']})"
                buttons = [
                    [Button.inline("✉️ Cek SMS", f"sms_{act_id}".encode()), Button.inline("📨 Semua SMS", f"smsall_{act_id}".encode())],
                    [Button.inline("✅ Selesai", f"fin_{act_id}".encode()), Button.inline("❌ Batal", f"can_{act_id}".encode())]
                ]
                await event.respond(text, buttons=buttons)
        else:
            await event.reply("ℹ️ Tidak ada aktivasi berjalan.")
