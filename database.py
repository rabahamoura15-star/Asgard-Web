import requests
import os
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()
class AsgardSystem:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.anilist_api = "https://graphql.anilist.co"
        self.supabase = None
        if self.url and self.key:
            try: self.supabase = create_client(self.url, self.key)
            except: pass
    def login(self, email, password):
        if not self.supabase: return "ERROR"
        try:
            data = self.supabase.auth.sign_in_with_password({"email": email, "password": password})
            if data.user: return "SUCCESS"
            return "ERROR"
        except: return "ERROR"
    def fetch_media(self, page, type_media, country=None):
        query = "query ($p: Int, $t: MediaType, $c: CountryCode) { Page(page: $p, perPage: 18) { media(type: $t, countryOfOrigin: $c, sort: TRENDING_DESC) { id title { english romaji } coverImage { extraLarge } description format status } } }"
        variables = {"p": page, "t": type_media}
        if country: variables["c"] = country
        try:
            r = requests.post(self.anilist_api, json={'query': query, 'variables': variables}, timeout=10)
            if r.status_code == 200: return r.json().get('data', {}).get('Page', {}).get('media', [])
            return []
        except: return []
