from config import ALLOWED_USERS

def is_allowed(event):
    """Filter untuk mengecek apakah sender_id ada di whitelist"""
    # Jika daftar kosong, izinkan semua (opsional). Jika diisi, wajib cocok.
    if not ALLOWED_USERS:
        return False # Set True jika ingin mode publik saat env kosong
    return event.sender_id in ALLOWED_USERS
