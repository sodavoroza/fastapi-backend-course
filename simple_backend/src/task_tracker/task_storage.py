import json
from pathlib import Path


class TaskStorage:
    def __init__(self, file_path="tasks.json"):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self._save_data({"tasks": []})

    def _load_data(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"tasks": []}  # Если файл повреждён, возвращаем пустой список

    def _save_data(self, data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_tasks(self):
        return self._load_data().get("tasks", [])

    def add_task(self, task):
        data = self._load_data()
        existing_ids = [t["id"] for t in data["tasks"]]
        task["id"] = max(existing_ids, default=0) + 1

        data["tasks"].append(task)
        self._save_data(data)

    def delete_task(self, task_id):
        data = self._load_data()
        data["tasks"] = [task for task in data["tasks"] if task["id"] != task_id]
        self._save_data(data)
