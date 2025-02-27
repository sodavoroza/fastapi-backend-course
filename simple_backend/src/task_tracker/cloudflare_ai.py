from base_http_client import BaseHTTPClient


class CloudflareAI(BaseHTTPClient):
    def __init__(self, api_url: str, api_key: str):
        super().__init__(api_url, api_key)

    def process_request(self, task_text: str) -> str:
        payload = {
            "model": "mistral",
            "messages": [
                {"role": "system", "content": "Ты помощник для решения задач."},
                {"role": "user", "content": f"Как решить задачу? {task_text}"},
            ],
        }

        response = self._send_request("POST", "ai/v1/chat", payload)

        choices = response.get("choices", [])
        if not choices or not isinstance(choices, list) or "message" not in choices[0]:
            return "Ошибка: AI не вернул корректный ответ."

        return choices[0]["message"].get("content", "Нет ответа")
