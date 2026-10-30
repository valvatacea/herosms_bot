from telethon import events, Button
from hero_api import api
from utils import is_allowed, build_service_keyboard, build_country_keyboard

def register(client):
    @client.on(events.CallbackQuery(func=is_allowed))
    async def handler(event):
        data = event.data.decode('utf-8')
        
        # --- KEMBALI KE MENU UTAMA PEMBELIAN ---
        if data == "menu_buy_start":
            services = await api.get_all_services()
            buttons = build_service_keyboard(services, page=0)
            await event.edit("🛒 **Pilih Aplikasi / Layanan**\n\nSilakan pilih aplikasi yang ingin diregistrasi (Hal 1):", buttons=buttons)

        # --- 1. NAVIGASI HALAMAN LAYANAN/APLIKASI ---
        elif data.startswith("srv_p_"):
            page = int(data.split("_")[2])
            services = await api.get_all_services()
            buttons = build_service_keyboard(services, page=page)
            await event.edit(f"🛒 **Pilih Aplikasi / Layanan**\n\nSilakan pilih aplikasi (Hal {page+1}):", buttons=buttons)

        # --- 2. PILIH LAYANAN -> LANJUT KE PEMILIHAN NEGARA ---
        elif data.startswith("buy_s_"):
            service = data.split("_")[2]
            
            # Cari nama panjang aplikasi untuk UI
            s_name = service.upper()
            services = await api.get_all_services()
            for code, name in services:
                if code == service:
                    s_name = name
                    break
            
            countries = await api.get_all_countries()
            buttons = build_country_keyboard(service, countries, page=0)
            await event.edit(f"🛒 **Beli Nomor: {s_name}** (`{service}`)\n\nSilakan pilih negara tujuan:", buttons=buttons)

        # --- 3. NAVIGASI HALAMAN NEGARA ---
        elif data.startswith("buy_p_"):
            parts = data.split("_")
            service = parts[2]
            page = int(parts[3])
            
            countries = await api.get_all_countries()
            buttons = build_country_keyboard(service, countries, page=page)
            await event.edit(f"🛒 **Beli Nomor**\n\nSilakan pilih negara (Hal {page+1}):", buttons=buttons)

        # --- 4. PILIH NEGARA -> TAMPILKAN PILIHAN JUMLAH ---
        elif data.startswith("buy_c_"):
            parts = data.split("_")
            service = parts[2]
            country = parts[3]
            
            c_name = country
            countries = await api.get_all_countries()
            for cid, name in countries:
                if cid == country:
                    c_name = name
                    break
            
            buttons = [
                [Button.inline("1 Nomor", f"buy_a_{service}_{country}_1".encode()), Button.inline("2 Nomor", f"buy_a_{service}_{country}_2".encode())],
                [Button.inline("5 Nomor", f"buy_a_{service}_{country}_5".encode()), Button.inline("10 Nomor", f"buy_a_{service}_{country}_10".encode())],
                [Button.inline("⬅️ Ganti Negara", f"buy_s_{service}".encode()), Button.inline("❌ Batal", b"buy_cancel")]
            ]
            await event.edit(f"🛒 **Beli Nomor**\nLayanan: `{service}`\nNegara: **{c_name}**\n\nPilih jumlah nomor (Maks 10):", buttons=buttons)

        # --- 5. PILIH JUMLAH -> TAMPILKAN KONFIRMASI ---
        elif data.startswith("buy_a_"):
            parts = data.split("_")
            service = parts[2]
            country = parts[3]
            amount = parts[4]
            
            buttons = [
                [Button.inline("✅ Ya, Konfirmasi Beli", f"buy_y_{service}_{country}_{amount}".encode())],
                [Button.inline("⬅️ Ganti Jumlah", f"buy_c_{service}_{country}".encode()), Button.inline("❌ Batal", b"buy_cancel")]
            ]
            await event.edit(f"⚠️ **KONFIRMASI PEMBELIAN**\n\nLayanan: `{service}`\nNegara ID: `{country}`\nJumlah Beli: `{amount}` Nomor\n\nLanjutkan transaksi ini?", buttons=buttons)

        # --- 6. EKSEKUSI PEMBELIAN (API V1) ---
        elif data.startswith("buy_y_"):
            parts = data.split("_")
            service = parts[2]
            country = parts[3]
            amount = int(parts[4])
            
            await event.edit("🔄 Memproses pembelian ke server, mohon tunggu...")
            payload = {"service": service, "country": int(country), "amount": amount}
            status, res = await api.request_v1('POST', '/activations', json=payload)
            
            if status == 200 and "data" in res:
                data_list = res["data"]
                text = f"✅ **Sukses Membeli {len(data_list)} Nomor!**\n\n"
                
                for act in data_list:
                    text += f"🆔 `{act['id']}` | 📱 `+{act['phone']}` | 💰 ${act['price']}\n"
                
                if len(data_list) == 1:
                    act_id = data_list[0]['id']
                    buttons = [
                        [Button.inline("✉️ Cek SMS", f"sms_{act_id}".encode()), Button.inline("📨 Semua SMS", f"smsall_{act_id}".encode())],
                        [Button.inline("✅ Selesai", f"fin_{act_id}".encode()), Button.inline("❌ Batal", f"can_{act_id}".encode())]
                    ]
                    await event.edit(text, buttons=buttons)
                else:
                    text += "\nℹ️ *Gunakan /active di menu utama untuk melihat pesan masing-masing nomor.*"
                    await event.edit(text)
            else:
                title = res.get('title', 'ERROR') if isinstance(res, dict) else 'ERROR'
                await event.edit(f"❌ Gagal membeli (Code: {status})\nAlasan: `{title}`")
                
        # --- 7. BATAL GLOBAL ---
        elif data == "buy_cancel":
            await event.edit("❌ Proses pembelian dibatalkan.")
