from telethon import events
from hero_api import api
from utils import is_allowed

def register(client):
    @client.on(events.NewMessage(pattern=r'(?i)^/sms\s+(\d+)$', func=is_allowed))
    async def sms(event):
        act_id = event.pattern_match.group(1)
        status, res = await api.request_v1('GET', f'/activations/{act_id}/otp/last')
        if status == 200 and res.get("data"):
            data = res["data"]
            await event.reply(f"✉️ **OTP:** `{data.get('smsCode', '-')}`\n📝 Teks: {data.get('smsText', '-')}")
        else:
            await event.reply("⏳ Belum ada SMS (Atau ID Salah).")

    @client.on(events.NewMessage(pattern=r'(?i)^/sms_all\s+(\d+)$'))
    async def sms_all(event):
        act_id = event.pattern_match.group(1)
        status, res = await api.request_v1('GET', f'/activations/{act_id}/otp')
        if status == 200 and res.get("data"):
            text = "\n".join([f"🔹 `{m.get('smsCode', '-')}` - {m.get('smsText', '-')}" for m in res["data"]])
            await event.reply(f"📨 **Semua SMS ID {act_id}:**\n{text}")
        else:
            await event.reply("⏳ Belum ada SMS.")
