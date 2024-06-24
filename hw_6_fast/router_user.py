from fastapi import APIRouter, HTTPException
from models import User, UserIn
from db import database, users

router = APIRouter()

@router.post("/users/")        # добавляет нового пользователя.
async def add_user(new_user : UserIn):
    query = users.insert().values(name = new_user.name,
                                  last_name = new_user.last_name,
                                  email = new_user.email,
                                  password = new_user.password )
    last_user_id = await database.execute(query)
    return {**new_user.dict(), "id" : last_user_id}

@router.post("/users/{count}")        # добавляет несколько пользователей.
async def add_users(count: int):
    for i in range(1, count+1):
        query = users.insert().values(name = f'user_{i}',
                                  last_name = f'last_name_{i}',
                                  email = f'mail_{i}@mail.ru',
                                  password = f'pass{i}' )
        await database.execute(query)
    return {'message': f'{count} new users create'}

@router.get("/users/{user_id}", response_model=User)     # возвращает пользователя с указанным идентификатором.
async def show_user(user_id : int):
    query = users.select().where(users.c.id == user_id)
    if not (await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail="User not found")
    return await database.fetch_one(query)

@router.put("/users/{user_id}")         # обновляет пользователя с указанным идентификатором.
async def edit_user(user_id : int, new_user : UserIn):
    query = users.select().where(users.c.id == user_id)
    if not (await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail="User not found")
    query = users.update().where(users.c.id == user_id).values(
                                  name = new_user.name,
                                  last_name = new_user.last_name,
                                  email = new_user.email,
                                  password = new_user.password )
    await database.execute(query) 
    return {**new_user.dict()}

@router.delete("/users/{user_id}")      # удаляет пользователя с указанным идентификатором.
async def delete_user(user_id : int):
    query = users.select().where(users.c.id == user_id)
    if not (await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail="User not found")
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}