import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'coffee.db')

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    try:
        yield cursor, conn
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, description TEXT)")
    cursor.execute("SELECT COUNT(*) FROM menu")
    if cursor.fetchone()[0] == 0:
        menu_items = [
            (1, "Американо", 149, "Американо - напиток, приготовленный путём разбавления эспрессо горячей водой в определённой пропорции."),
            (2, "Раф", 211, "Раф - популярный российский кофейный напиток, который готовят на основе эспрессо с добавлением ванильного и простого сахара, а также сливок."),
            (3, "Латте", 219, "Латте - кофейный напиток на основе молока, представляющий собой трёхслойную смесь из молочной пены, молока и кофе эспрессо."),
            (4, "Капучино", 189, "Капучино - кофейный напиток итальянской кухни на основе эспрессо с добавлением в него подогретого до 65 градусов вспененного молока.")
        ]
        cursor.executemany("INSERT INTO menu (id, name, price, description) VALUES (?, ?, ?, ?)", menu_items)
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE, password TEXT, role TEXT DEFAULT 'customer')")
    cursor.execute("""CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT, 
        item_id INT, 
        cups INT, 
        cost REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    conn.close()