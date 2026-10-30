import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID', 0))
API_HASH = os.getenv('API_HASH', '')
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
HEROSMS_API_KEY = os.getenv('HEROSMS_API_KEY', '')

# Mengambil list User ID yang diizinkan
_users = os.getenv('ALLOWED_USERS', '')
ALLOWED_USERS = [int(x.strip()) for x in _users.split(',') if x.strip()]
