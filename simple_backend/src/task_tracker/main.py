from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from task_storage import TaskStorage
from cloudflare_ai import CloudflareAI
from cloud_storage import CloudStorage
import os
from dotenv import load_dotenv

load_dotenv()

CLOUDFLARE_API_URL = os.getenv("CLOUDFLARE_API_URL")
CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_KEY")
JSONBIN_API_KEY = os.getenv("JSONBIN_API_KEY")
JSONBIN_BIN_ID = os.getenv("JSONBIN_BIN_ID")

if not all([CLOUDFLARE_API_URL, CLOUDFLARE_API_KEY, JSONBIN_API_KEY, JSONBIN_BIN_ID]):
    raise ValueError("Ошибка: Не заданы переменные окружения для API!")

app = FastAPI()

storage = TaskStorage()
ai = CloudflareAI(CLOUDFLARE_API_URL, CLOUDFLARE_API_KEY)
cloud_storage = CloudStorage(
    "https://api.jsonbin.io/v3", JSONBIN_API_KEY, JSONBIN_BIN_ID
)


class Task(BaseModel):
    title: str
    status: str
    description: str


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return storage.get_tasks()


@app.post("/tasks")
def create_task(task: Task):
    try:
        solution = ai.process_request(task.description)
        new_task = {
            "title": task.title,
            "status": task.status,
            "description": f"{task.description}\n\nРешение:\n{solution}",
        }

        storage.add_task(new_task)
        cloud_storage.save_tasks(storage.get_tasks())

        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    storage.delete_task(task_id)
    cloud_storage.save_tasks(storage.get_tasks())
    return {"message": "Задача удалена"}
