from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import requests
import time

"""
список задач. Каждая задача должна содержать заголовок и описание. Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).

API должен содержать следующие конечные точки:
 — GET /tasks — возвращает список всех задач.
 — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
 — POST /tasks — добавляет новую задачу.
 — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
 — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку Pydantic.
"""

app = FastAPI()

class Task(BaseModel):
    id : int
    title : str
    decription : str

tasks = [
  {
    "id": 1,
    "title": "task_1",
    "decription": "desc_task1"
  },
  {
    "id": 2,
    "title": "task_2",
    "decription": "desc_task2"
  },
  {
    "id": 3,
    "title": "task_3",
    "decription": "desc_task3"
  }
]
#curr_id = 1

"""
def find_id():      # Функция определения максимального ID
    if not task:
        return 1
    else:
        max_id = 0
        for task in tasks:
            if task.id > max_id:
                max_id = task.id
        return max_id+1
"""


@app.get("/")
async def root():
    return {"message" : "let's start"}

@app.get("/tasks/")         # возвращает список всех задач.
async def show_all_tasks():
    return tasks

@app.get("/tasks/{id}")     # возвращает задачу с указанным идентификатором.
async def show_task(id : int):
    for task in tasks:
        if task['id'] == id:
            return task
    return {"message" : "Task not found"}

@app.post("/tasks/")        # добавляет новую задачу.
async def add_task(task : Task):
    tasks.append(task)
    return {"message" : "add new task"}

@app.put("/tasks/{id}")         # обновляет задачу с указанным идентификатором.
async def edit_task(id : int, new_task : Task):
    for i in range(len(tasks)):
        if tasks[i]['id'] == id:
            tasks[i]['title'] = new_task.title
            tasks[i]['decription'] = new_task.decription
            return {"message" : "edit task"}
    return {"message" : "Task not found"}

@app.delete("/tasks/{id}")      # удаляет задачу с указанным идентификатором.
async def delete_task(id : int):
    for i in range(len(tasks)):
        if tasks[i]['id'] == id:
            print('____',i)
            del tasks[i]
            return {"message" : "delete task"}
    return {"message" : "Task not found"}

if __name__ =='__main__':
    pass