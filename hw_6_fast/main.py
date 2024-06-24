from fastapi import FastAPI
import router_user, router_item, router_order
from db import database
import uvicorn

"""
Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.

• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.
• Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
• Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.
"""

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "let's start"}

app.include_router(router_user.router, tags=['user'])
app.include_router(router_item.router, tags=['item'])
app.include_router(router_order.router, tags=['order'])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ =='__main__':
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)