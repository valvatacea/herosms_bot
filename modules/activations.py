from telethon import events
from hero_api import api

def format_error(status, data):
    title = data.get('title', 'ERROR') if isinstance(data, dict) else 'ERROR'
    return f"❌ Gagal (Code: {status})\nAlasan: `{title}`"

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^/buy\s+([a-zA-Z]+)\s+(\d+)$'))
    async def buy(event):
        service, country = event.pattern_match.groups()
        payload = {"service": service.lower(), "country": int(country), "amount": 1}
        msg = await event.reply("🔄 Memproses...")
        
        status, res = await api.request_v1('POST', '/activations', json=payload)
        if status == 200 and "data" in res:
            act = res["data"][0]
            await msg.edit(f"✅ **Sukses Beli!**\n🆔 ID: `{act['id']}`\n📱 Nomor: `+{act['phone']}`\n💰 Harga: ${act['price']}")
        else:
            await msg.edit(format_error(status, res))

    @client.on(events.NewMessage(pattern=r'(?i)^/cancel\s+(\d+)$'))
    async def cancel(event):
        act_id = event.pattern_match.group(1)
        status, res = await api.request_v1('DELETE', f'/activations/{act_id}')
        await event.reply("✅ Aktivasi dibatalkan." if status == 204 else format_error(status, res))

    @client.on(events.NewMessage(pattern=r'(?i)^/finish\s+(\d+)$'))
    async def finish(event):
        act_id = event.pattern_match.group(1)
        status, res = await api.request_v1('POST', f'/activations/{act_id}/finish')
        await event.reply("✅ Aktivasi diselesaikan." if status == 204 else format_error(status, res))

    @client.on(events.NewMessage(pattern=r'(?i)^/replace\s+(\d+)$'))
    async def replace(event):
        act_id = event.pattern_match.group(1)
        status, res = await api.request_v1('POST', f'/activations/{act_id}/replace')
        if status == 200:
            act = res["data"][0]
            await event.reply(f"🔄 **Nomor Diganti**\n🆔 ID Baru: `{act['id']}`\n📱 Nomor Baru: `+{act['phone']}`")
        else:
            await event.reply(format_error(status, res))

    @client.on(events.NewMessage(pattern=r'(?i)^/reactivate\s+(\d+)$'))
    async def reactivate(event):
        act_id = event.pattern_match.group(1)
        status, res = await api.request_v1('POST', f'/activations/{act_id}/reactivate')
        await event.reply("✅ Nomor berhasil direaktivasi." if status == 200 else format_error(status, res))

    @client.on(events.NewMessage(pattern=r'(?i)^/prolong\s+(\d+)\s+(\d+)$'))
    async def prolong(event):
        act_id, hours = event.pattern_match.groups()
        payload = {"duration": int(hours)}
        status, res = await api.request_v1('POST', f'/activations/{act_id}/prolong', json=payload)
        await event.reply(f"✅ Diperpanjang {hours} jam." if status == 200 else format_error(status, res))

    @client.on(events.NewMessage(pattern='(?i)^/active$'))
    async def active(event):
        status, res = await api.request_v1('GET', '/activations?size=10')
        if status == 200 and res.get("data"):
            text = "\n".join([f"🆔 `{a['id']}` | 📱 `+{a['phone']}` ({a['service']})" for a in res["data"]])
            await event.reply(f"📋 **Aktivasi Berjalan:**\n{text}")
        else:
            await event.reply("ℹ️ Tidak ada aktivasi berjalan.")

    @client.on(events.NewMessage(pattern='(?i)^/history$'))
    async def history(event):
        status, res = await api.request_v1('GET', '/activations/history?size=5&sort[id]=desc')
        if status == 200 and res.get("data"):
            text = "\n".join([f"🆔 `{a['id']}` | 📱 `+{a['phone']}` | ${a['cost']}" for a in res["data"]])
            await event.reply(f"🕒 **Riwayat Terakhir:**\n{text}")
        else:
            await event.reply("ℹ️ Riwayat kosong.")
