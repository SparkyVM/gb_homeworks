from fastapi import APIRouter, HTTPException
from datetime import datetime 
from models import Order, OrderIn
from db import database, users, items, orders
from random import choice

router = APIRouter()


@router.post("/orders/")        # добавляет новый заказ.
async def add_order(new_order : OrderIn):
    query = users.select().where(users.c.id == new_order.id_user)
    users_check = await database.fetch_one(query)                   # проверка пользователя в таблице
    query = items.select().where(items.c.id == new_order.id_item)
    items_check = await database.fetch_one(query)                   # проверка товара в таблице
    if users_check and items_check:
        query = orders.insert().values(status = new_order.status,
                                  id_user = new_order.id_user,
                                  id_item = new_order.id_item,
                                  created_at = new_order.created_at  )
        last_order_id = await database.execute(query)
        return {**new_order.dict(), "id" : last_order_id}
    else:
        raise HTTPException(status_code=404, detail="ID not found")

@router.post("/orders/{count}")        # добавляет несколько заказов.
async def add_orders(count: int):
    users_data = await database.fetch_all(users.select())
    items_data = await database.fetch_all(items.select())
    list_user_id =[]            # список ID пользователей
    list_item_id =[]            # список ID товаров
    for record in users_data: 
        list_user_id.append(record['id']) 
    for record in items_data: 
        list_item_id.append(record['id'])
    for i in range(1, count+1):
        query = orders.insert().values(status = 'new',
                                  id_user = choice(list_user_id),
                                  id_item = choice(list_item_id),
                                  created_at = datetime.now())
        await database.execute(query)
    return {'message': f'{count} new orders create'}    

@router.get("/orders/{order_id}", response_model=Order)     # возвращает заказ с указанным идентификатором.
async def show_order(order_id : int):
    query = orders.select().where(orders.c.id == order_id)
    if not (await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail="Order not found")
    return await database.fetch_one(query)

@router.put("/orders/{order_id}")           # обновляет заказ с указанным идентификатором.
async def edit_order(order_id : int, new_order : OrderIn):
    query = orders.select().where(orders.c.id == order_id)
    if not (await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail="Order not found")
    query = users.select().where(users.c.id == new_order.id_user)
    users_check = await database.fetch_one(query)                   # проверка пользователя в таблице
    query = items.select().where(items.c.id == new_order.id_item)
    items_check = await database.fetch_one(query)                   # проверка товара в таблице
    if users_check and items_check:
        query = orders.update().where(orders.c.id == order_id).values(
                                  status = new_order.status,
                                  id_user = new_order.id_user,
                                  id_item = new_order.id_item,
                                  created_at = new_order.created_at )
        await database.execute(query) 
        return {**new_order.dict()}
    else:
        raise HTTPException(status_code=404, detail="ID not found")

@router.delete("/orders/{order_id}")      # удаляет заказ с указанным идентификатором.
async def delete_order(order_id : int):
    query = orders.select().where(orders.c.id == order_id)
    if not (await database.fetch_one(query)):
        raise HTTPException(status_code=404, detail="Order not found")
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}