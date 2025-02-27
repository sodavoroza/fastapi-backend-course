from base_http_client import BaseHTTPClient


class CloudStorage(BaseHTTPClient):
    def __init__(self, api_url: str, api_key: str, bin_id: str):
        super().__init__(api_url, api_key)
        self.bin_id = bin_id

    def get_tasks(self):
        response = self._send_request("GET", f"b/{self.bin_id}")
        if isinstance(response, dict) and "record" in response:
            return response["record"] or []  # Если record пуст, возвращаем []
        return []

    def save_tasks(self, tasks):
        return self._send_request("PUT", f"b/{self.bin_id}", {"record": tasks})
