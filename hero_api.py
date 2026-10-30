import aiohttp
import json
from config import HEROSMS_API_KEY

class HeroSMS:
    def __init__(self):
        self.v1_url = "https://hero-sms.com/api/v1"
        self.stub_url = "https://hero-sms.com/stubs/handler_api.php"
        self.headers = {
            "Authorization": f"ApiKey {HEROSMS_API_KEY}",
            "Content-Type": "application/json"
        }
        self.country_cache = []
        self.service_cache = [] # Cache daftar layanan

    async def request_v1(self, method, endpoint, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self.v1_url}{endpoint}", headers=self.headers, **kwargs) as resp:
                status = resp.status
                try:
                    data = await resp.json()
                except Exception:
                    data = await resp.text()
                return status, data

    async def request_stub(self, action, **params):
        params['api_key'] = HEROSMS_API_KEY
        params['action'] = action
        async with aiohttp.ClientSession() as session:
            async with session.get(self.stub_url, params=params) as resp:
                return await resp.text()

    async def get_all_countries(self):
        if self.country_cache:
            return self.country_cache
            
        res = await self.request_stub("getCountries")
        try:
            data = json.loads(res)
            if isinstance(data, dict):
                countries = [(str(v['id']), v.get('eng', str(v['id']))) for k, v in data.items()]
            elif isinstance(data, list):
                countries = [(str(item['id']), item.get('eng', str(item['id']))) for item in data]
            else:
                countries = []
                
            countries.sort(key=lambda x: x[1])
            self.country_cache = countries
            return self.country_cache
        except Exception as e:
            print("Error parsing countries:", e)
            return []

    async def get_all_services(self):
        """Mengambil dan menyimpan daftar layanan aplikasi secara dinamis dari API[span_1](start_span)[span_1](end_span)"""
        if self.service_cache:
            return self.service_cache
            
        res = await self.request_stub("getServicesList")
        try:
            data = json.loads(res)
            # Format respons API biasanya berisi list layanan dengan 'code' dan 'name'
            services_list = data.get('services', []) if isinstance(data, dict) else data
            
            services = []
            for item in services_list:
                code = item.get('code')
                name = item.get('name')
                if code and name:
                    services.append((code, name))
                    
            services.sort(key=lambda x: x[1])
            self.service_cache = services
            return self.service_cache
        except Exception as e:
            print("Error parsing services:", e)
            return []

api = HeroSMS()
