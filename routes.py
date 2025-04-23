from fastapi import FastAPI, HTTPException, Depends

from .utils import verify_token, verify_admin, pwd_context
from .db import get_db
from .schemas import Item, User
from .services import calculate_order_cost, format_order_message

app = FastAPI(title="Coffee Shop", description="API для Coffee shop")


@app.get("/hello")
async def greeting():
    return {"message": "Добро пожаловать в Coffee shop!"}

@app.post("/register")
async def register(user: User, db = Depends(get_db)):
    cursor, conn = db
    user_password = pwd_context.hash(user.password)
    cursor.execute("SELECT username FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Такой пользователь уже существует, пожалуйста выберите другой логин")
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (user.username, user_password, 'customer'))
    conn.commit()
    return {"message": "Пользователь создан"}

@app.post('/login')
async def login(user: User, db = Depends(get_db)):
    cursor, conn = db
    cursor.execute("SELECT username, password, role FROM users WHERE username = ?", (user.username,))
    result = cursor.fetchone()
    if not result or not pwd_context.verify(user.password, result[1]):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    role = result[2]
    from .utils import create_token
    token = create_token(user.username, role)
    return token

@app.get("/menu")
async def get_menu(db = Depends(get_db)):
    cursor, conn = db
    cursor.execute('SELECT id, name, price, description FROM menu')
    result = cursor.fetchall()
    menu = [{'id': item[0], 'name': item[1], 'price': item[2], 'description': item[3]} for item in result]
    if menu:
        return menu
    return {'message': 'Меню пусто'}

@app.get("/menu/{item_id}")
async def get_drink(item_id: int, db = Depends(get_db)):
    cursor, conn = db
    cursor.execute('SELECT id, name, price, description FROM menu WHERE id = ?', (item_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Напиток не найден")
    return {'id': result[0], 'name': result[1], 'price': result[2], 'description': result[3]}

@app.post("/order")
async def order(item: Item, user: dict = Depends(verify_token), db = Depends(get_db)):
    cursor, conn = db
    cursor.execute('SELECT id, name, price, description FROM menu WHERE id = ?', (item.item_id,))
    drink = cursor.fetchone()
    if not drink:
        raise HTTPException(status_code=404, detail="Напиток не найден")
    cost = calculate_order_cost(drink, item.cups)
    cursor.execute("INSERT INTO orders (username, item_id, cups, cost) VALUES (?, ?, ?, ?)", (user['username'], item.item_id, item.cups, cost))
    conn.commit()
    return {"message": format_order_message(drink, item.cups, cost)}

@app.get("/my_orders")
async def my_orders(user: dict = Depends(verify_token), db = Depends(get_db)):
    cursor, conn = db
    cursor.execute("SELECT id, item_id, cups, cost, created_at FROM orders WHERE username = ?", (user['username'],))
    rows = cursor.fetchall()
    if not rows:
        return {'message': 'Пока нет заказов', "total_cost": 0}
    user_orders = [
        {
            'id': row[0],
            'item_id': row[1],
            'cups': row[2],
            'cost': row[3],
            'created_at': row[4],
            'name': 'Неизвестный напиток' if not (drink := cursor.execute("SELECT id, name, price, description FROM menu WHERE id = ?", (row[1],)).fetchone()) else drink[1]
        }
        for row in rows
    ]
    total_cost = sum(order['cost'] for order in user_orders)
    return {"orders": user_orders, "total_cost": total_cost}

@app.get('/admin/orders')
async def get_all_orders(limit: int = 10, offset: int = 0, _: dict = Depends(verify_admin), db = Depends(get_db)):
    cursor, conn = db
    row_orders = cursor.execute('SELECT * FROM orders').fetchall()
    user_orders = [
        {
            'id': row[0],
            'username': row[1],
            'name': 'Неизвестный напиток' if not (drink := cursor.execute("SELECT id, name, price, description FROM menu WHERE id = ?", (row[2],)).fetchone()) else drink[1],
            'item_id': row[2],
            'cups': row[3],
            'cost': row[4],
            'created_at': row[5]
        }
        for row in row_orders
    ]
    if user_orders:
        return {'orders': user_orders}
    return {'message': 'Пока нет заказов'}