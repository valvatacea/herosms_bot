from config import ALLOWED_USERS
from telethon import Button

def is_allowed(event):
    if not ALLOWED_USERS:
        return False
    return event.sender_id in ALLOWED_USERS

def build_service_keyboard(services_list, page=0, per_page=12):
    """Menghasilkan tombol layanan/aplikasi berdasarkan halaman (12 per halaman)"""
    total_pages = max(1, (len(services_list) - 1) // per_page + 1)
    
    start_idx = page * per_page
    end_idx = start_idx + per_page
    current_services = services_list[start_idx:end_idx]
    
    buttons = []
    row = []
    
    # Render tombol aplikasi (2 kolom)
    for code, name in current_services:
        display_name = (name[:16] + '..') if len(name) > 18 else name
        row.append(Button.inline(display_name, f"buy_s_{code}".encode()))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
        
    # Baris Navigasi Halaman Layanan
    nav_row = []
    if page > 0:
        nav_row.append(Button.inline("⬅️ Prev", f"srv_p_{page-1}".encode()))
    if page < total_pages - 1:
        nav_row.append(Button.inline("Next ➡️", f"srv_p_{page+1}".encode()))
        
    if nav_row:
        buttons.append(nav_row)
        
    buttons.append([Button.inline("❌ Batal", b"buy_cancel")])
    return buttons

def build_country_keyboard(service, countries_list, page=0, per_page=14):
    total_pages = max(1, (len(countries_list) - 1) // per_page + 1)
    start_idx = page * per_page
    end_idx = start_idx + per_page
    current_countries = countries_list[start_idx:end_idx]
    
    buttons = []
    row = []
    for cid, cname in current_countries:
        display_name = (cname[:13] + '..') if len(cname) > 15 else cname
        row.append(Button.inline(display_name, f"buy_c_{service}_{cid}".encode()))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
        
    nav_row = []
    if page > 0:
        nav_row.append(Button.inline("⬅️ Prev", f"buy_p_{service}_{page-1}".encode()))
    if page < total_pages - 1:
        nav_row.append(Button.inline("Next ➡️", f"buy_p_{service}_{page+1}".encode()))
        
    if nav_row:
        buttons.append(nav_row)
        
    # Tombol kembali ke menu pemilihan layanan
    buttons.append([Button.inline("⬅️ Ganti Aplikasi", b"menu_buy_start"), Button.inline("❌ Batal", b"buy_cancel")])
    return buttons
