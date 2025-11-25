import os
import json

import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()


class UbersuggestClient:
    """
    Cliente simples para o endpoint interno /api/match_keywords do Ubersuggest.
    Usa os dados da sua sessão (token, x-ubs-data, cookies, user-agent).
    """

    BASE_URL = "https://app.neilpatel.com/api/match_keywords"

    def __init__(self) -> None:
        self.auth_token = os.getenv("UBS_AUTH_TOKEN", "").strip()
        self.x_ubs_data = os.getenv("UBS_X_UBS_DATA", "").strip()
        self.cookies_header = os.getenv("UBS_COOKIES_HDR", "").strip()
        self.user_agent = os.getenv("UBS_USER_AGENT", "").strip()

        if not self.auth_token:
            raise ValueError("UBS_AUTH_TOKEN não definido no .env")
        if not self.x_ubs_data:
            raise ValueError("UBS_X_UBS_DATA não definido no .env")
        if not self.cookies_header:
            raise ValueError("UBS_COOKIES_HDR não definido no .env")
        if not self.user_agent:
            raise ValueError("UBS_USER_AGENT não definido no .env")

    def match_keywords(
        self,
        keyword: str,
        lang: str = "pt",
        loc_id: str = "2076",
        limit: int = 300,
        sortby: str = "-searchVolume",
    ) -> dict:
        """
        Faz um POST para /api/match_keywords com a keyword base.
        Retorna o JSON bruto da API.
        """
        payload = {
            "keywords": [keyword],
            "locId": str(loc_id),
            "language": lang,
            "sortby": sortby,
            "limit": limit,
            "previousKey": 0,
            "filters": {},
            "domain": "",
        }

        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "User-Agent": self.user_agent,
            "x-ubs-data": self.x_ubs_data,
            "Cookie": self.cookies_header,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://app.neilpatel.com",
            "Referer": "https://app.neilpatel.com/pt/ubersuggest/keyword_ideas/",
        }

        resp = requests.post(self.BASE_URL, headers=headers, json=payload)
        resp.raise_for_status()

        try:
            return resp.json()
        except Exception:
            return {"error": "Falha ao parsear JSON", "raw": resp.text}
