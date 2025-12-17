import sqlite3
from contextlib import closing
import os

# Use environment variable for database path with fallback
DB_PATH = os.environ.get('DB_PATH', 'db.sqlite')

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with closing(get_conn()) as conn:
        c = conn.cursor()
        # feedback table
        c.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # products table
        c.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT
            )
        ''')
        # orders table
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                customer_email TEXT,
                status TEXT DEFAULT 'new',
                total REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # order_items table (many-to-many)
        c.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY(order_id) REFERENCES orders(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        ''')
        conn.commit()
    # insert sample products if empty
    if len(get_products()) == 0:
        sample_products = [
            ("Футболка Classic", "Бавовняна футболка, різні кольори.", 19.99, "https://picsum.photos/seed/t1/600/400"),
            ("Сорочка Formal", "Елегантна сорочка для офісу.", 39.99, "https://picsum.photos/seed/t2/600/400"),
            ("Куртка Cozy", "Тепла куртка на холодну погоду.", 89.99, "https://picsum.photos/seed/t3/600/400"),
            ("Штани Slim", "Стильні вузькі штани.", 49.99, "https://picsum.photos/seed/t4/600/400"),
            ("Сукня Summer", "Легка літня сукня.", 59.99, "https://picsum.photos/seed/t5/600/400"),
            ("Кепка Sport", "Кепка для спорту та прогулянок.", 14.99, "https://picsum.photos/seed/t6/600/400"),
        ]
        for p in sample_products:
            add_product(*p)

# Feedback operations
def add_feedback(name, email, message):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)', (name, email, message))
        conn.commit()
        return c.lastrowid

def get_feedbacks():
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM feedback ORDER BY created_at DESC')
        return c.fetchall()

def get_feedback(feedback_id):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM feedback WHERE id=?', (feedback_id,))
        return c.fetchone()

def delete_feedback(feedback_id):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM feedback WHERE id=?', (feedback_id,))
        conn.commit()

# Product operations
def add_product(title, description, price, image_url=None):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO products (title, description, price, image_url) VALUES (?, ?, ?, ?)',
                  (title, description, price, image_url))
        conn.commit()
        return c.lastrowid

def update_product(product_id, title, description, price, image_url):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('UPDATE products SET title=?, description=?, price=?, image_url=? WHERE id=?',
                  (title, description, price, image_url, product_id))
        conn.commit()

def delete_product(product_id):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM products WHERE id=?', (product_id,))
        conn.commit()

def get_products(limit=None):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        q = 'SELECT * FROM products ORDER BY id DESC'
        if limit:
            q += f' LIMIT {int(limit)}'
        c.execute(q)
        return c.fetchall()

def get_product(product_id):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM products WHERE id=?', (product_id,))
        return c.fetchone()

# Orders and items
def create_order(customer_name, customer_email, total):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO orders (customer_name, customer_email, total) VALUES (?, ?, ?)',
                  (customer_name, customer_email, total))
        conn.commit()
        return c.lastrowid

def add_order_item(order_id, product_id, quantity, price):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                  (order_id, product_id, quantity, price))
        conn.commit()

def get_orders():
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM orders ORDER BY created_at DESC')
        return c.fetchall()

def get_order(order_id):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM orders WHERE id=?', (order_id,))
        return c.fetchone()

def get_order_items(order_id):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT oi.*, p.title, p.image_url FROM order_items oi
            LEFT JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id=?
        ''', (order_id,))
        return c.fetchall()

def update_order_status(order_id, status):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('UPDATE orders SET status=? WHERE id=?', (status, order_id))
        conn.commit()
