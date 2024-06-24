from fastapi import APIRouter, HTTPException
from models import Item, ItemIn
from db import database, items
from random import randint

router = APIRouter()


@router.post("/items/")        # добавляет новый товар.
async def add_item(new_item : ItemIn):
    query = items.insert().values(name = new_item.name,
                                  decription = new_item.decription,
                                  price = new_item.price)
    last_item_id = await database.execute(query)
    return {**new_item.dict(), "id" : last_item_id}

@router.post("/items/{count}")        # добавляет несколько товаров.
async def add_items(count: int):
    for i in range(1, count+1):
        query = items.insert().values(name = f'item_{i}',
                                  decription = f'decription_{i}',
                                  price = float(randint(100, 10_000)) )
        await database.execute(query)
    return {'message': f'{count} new items create'}

@router.get("/items/{item_id}", response_model=Item)     # возвращает товар с указанным идентификатором.
async def show_item(item_id : int):
    query = items.select().where(items.c.id == item_id)
    if not (await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail="Item not found")
    return await database.fetch_one(query)

@router.put("/items/{item_id}")         # обновляет товар с указанным идентификатором.
async def edit_item(item_id : int, new_item : ItemIn):
    query = items.select().where(items.c.id == item_id)
    if not (await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail="Item not found")
    query = items.update().where(items.c.id == item_id).values(
                                  name = new_item.name,
                                  decription = new_item.decription,
                                  price = new_item.price )
    await database.execute(query) 
    return {**new_item.dict()}

@router.delete("/items/{item_id}")      # удаляет товар с указанным идентификатором.
async def delete_user(item_id : int):
    query = items.select().where(items.c.id == item_id)
    if not (await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail="Item not found")
    query = items.delete().where(items.c.id == item_id)
    await database.execute(query)
    return {'message': 'Items deleted'}