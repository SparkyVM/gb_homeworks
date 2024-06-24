from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

# Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.
# Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
# Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.

class Item(BaseModel):
    id : int
    name : str = Field(..., title = "Name", max_length = 30)
    decription : str = Field(title = "Decription", max_length = 50)
    price : float = Field(title = "Price", gt = 0, le = 10000)

class User(BaseModel):
    id : int
    name : str = Field(..., title = "Name", max_length = 20)
    last_name : str = Field(title = "Last Name", max_length = 20)
    email : str = Field(..., title = "Email", max_length = 20)
    password : str = Field(..., title = "Password", min_length = 3, max_length = 8)

class Order(BaseModel):
    id : int
    id_user : int
    id_item : int
    created_at : datetime
    status : str = Field(..., title = "Status", max_length = 20)

class ItemIn(BaseModel):
    name : str = Field(..., title = "Name", max_length = 30)
    decription : str = Field(title = "Decription", max_length = 50)
    price : float = Field(title = "Price", gt = 0, le = 10000)

class UserIn(BaseModel):
    name : str = Field(..., title = "Name", max_length = 20)
    last_name : str = Field(title = "Last Name", max_length = 20)
    email : str = Field(..., title = "Email", max_length = 20)
    password : str = Field(..., title = "Password", min_length = 3, max_length = 8)

class OrderIn(BaseModel):
    id_user : int
    id_item : int
    created_at : datetime = datetime.now
    status : str = Field(..., title = "Status", max_length = 20)