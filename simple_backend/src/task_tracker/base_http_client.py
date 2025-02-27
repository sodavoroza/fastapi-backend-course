import requests
from abc import ABC, abstractmethod


class BaseHTTPClient(ABC):
    def __init__(self, api_url: str, api_key: str = None):
        self.api_url = api_url.rstrip("/")  # Убираем лишние слэши
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json",
        }

    def _send_request(self, method: str, endpoint: str, payload=None):
        """ Универсальный метод для запросов с обработкой ошибок. """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(method, url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса {method} {url}: {e}")
            return {"error": f"Ошибка сети: {str(e)}"}

    @abstractmethod
    def process_request(self, *args, **kwargs):
        pass
