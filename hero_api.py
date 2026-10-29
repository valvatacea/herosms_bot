import aiohttp
from config import HEROSMS_API_KEY

class HeroSMS:
    def __init__(self):
        self.v1_url = "https://hero-sms.com/api/v1"
        self.stub_url = "https://hero-sms.com/stubs/handler_api.php"
        self.headers = {
            "Authorization": f"ApiKey {HEROSMS_API_KEY}",
            "Content-Type": "application/json"
        }

    async def request_v1(self, method, endpoint, **kwargs):
        """Handle request ke HeroSMS V1 API"""
        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self.v1_url}{endpoint}", headers=self.headers, **kwargs) as resp:
                status = resp.status
                try:
                    data = await resp.json()
                except Exception:
                    data = await resp.text()
                return status, data

    async def request_stub(self, action, **params):
        """Handle request ke API kompatibel SMS-Activate"""
        params['api_key'] = HEROSMS_API_KEY
        params['action'] = action
        async with aiohttp.ClientSession() as session:
            async with session.get(self.stub_url, params=params) as resp:
                return await resp.text()

api = HeroSMS()
