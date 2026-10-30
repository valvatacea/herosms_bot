from telethon import events
from hero_api import api
from utils import is_allowed

def register(client):
    # Callback query juga dilindungi oleh fungsi is_allowed
    @client.on(events.CallbackQuery(func=is_allowed))
    async def handler(event):
        data = event.data.decode('utf-8')
        
        # --- MENU UTAMA ---
        if data == "menu_balance":
            res = await api.request_stub("getBalance")
            if "ACCESS_BALANCE" in res:
                await event.answer(f"Saldo Anda: ${res.split(':')[1]}", alert=True)
            else:
                await event.answer("Gagal mengambil saldo.", alert=True)
                
        elif data == "menu_active":
            await event.answer("Menampilkan daftar aktivasi...")
            # Mengirim perintah /active ke bot itu sendiri agar memicu handler active
            await client.send_message(event.chat_id, "/active")
            
        elif data == "menu_history":
            await event.answer("Mengambil riwayat...")
            status, res = await api.request_v1('GET', '/activations/history?size=5&sort[id]=desc')
            if status == 200 and res.get("data"):
                text = "🕒 **Riwayat Terakhir:**\n\n" + "\n".join([f"🆔 `{a['id']}` | 📱 `+{a['phone']}` | ${a['cost']}" for a in res["data"]])
                await event.respond(text)
            else:
                await event.answer("Riwayat kosong / Error", alert=True)
                
        elif data == "menu_help_buy":
            await event.answer("Ketik: /buy <kode_layanan> <kode_negara>", alert=True)

        # --- AKSI PADA NOMOR (CEK SMS, SELESAI, BATAL) ---
        elif data.startswith("sms_"):
            act_id = data.split("_")[1]
            status, res = await api.request_v1('GET', f'/activations/{act_id}/otp/last')
            if status == 200 and res.get("data"):
                d = res["data"]
                text = f"✉️ **OTP (ID {act_id}):**\n\n🔢 Kode: `{d.get('smsCode', '-')}`\n📝 Teks: {d.get('smsText', '-')}"
                await event.respond(text)
                await event.answer("SMS ditemukan!")
            else:
                await event.answer("Belum ada SMS masuk.", alert=False)
                
        elif data.startswith("smsall_"):
            act_id = data.split("_")[1]
            status, res = await api.request_v1('GET', f'/activations/{act_id}/otp')
            if status == 200 and res.get("data"):
                text = f"📨 **Semua SMS (ID {act_id}):**\n\n" + "\n".join([f"🔹 `{m.get('smsCode', '-')}` - {m.get('smsText', '-')}" for m in res["data"]])
                await event.respond(text)
            else:
                await event.answer("Belum ada SMS.", alert=False)
                
        elif data.startswith("fin_"):
            act_id = data.split("_")[1]
            status, _ = await api.request_v1('POST', f'/activations/{act_id}/finish')
            if status == 204:
                await event.edit(f"✅ Aktivasi `{act_id}` diselesaikan.")
            else:
                await event.answer(f"Gagal menyelesaikan (Code: {status})", alert=True)
                
        elif data.startswith("can_"):
            act_id = data.split("_")[1]
            status, _ = await api.request_v1('DELETE', f'/activations/{act_id}')
            if status == 204:
                await event.edit(f"❌ Aktivasi `{act_id}` dibatalkan. Saldo refund.")
            else:
                await event.answer(f"Gagal/Telat Batal (Code: {status})", alert=True)
