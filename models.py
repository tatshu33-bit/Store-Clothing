import sqlite3
from contextlib import closing

DB_PATH = "db.sqlite"

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
        # categories table
        c.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            )
        ''')
        # products table
        c.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT,
                category_id INTEGER,
                rating REAL DEFAULT 0.0,
                stock INTEGER DEFAULT 0,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        ''')
        # orders table
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                customer_email TEXT,
                customer_phone TEXT,
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
        # reviews table
        c.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                customer_name TEXT,
                rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        ''')
        conn.commit()
    # insert sample categories if empty
    if len(get_categories()) == 0:
        sample_categories = [
            ("Футболки та топи", "Повсякденний верхній одяг"),
            ("Сорочки", "Офіційний та casual одяг"),
            ("Куртки та пальта", "Верхній одяг для різних сезонів"),
            ("Штани та джинси", "Нижній одяг"),
            ("Сукні", "Жіночий одяг"),
            ("Аксесуари", "Доповнення до образу"),
        ]
        for name, desc in sample_categories:
            add_category(name, desc)
    
    # insert sample products if empty
    if len(get_products()) == 0:
        # Get category IDs
        categories = get_categories()
        cat_dict = {cat['name']: cat['id'] for cat in categories}
        
        sample_products = [
            ("Футболка Classic", "Бавовняна футболка, різні кольори.", 19.99, "https://picsum.photos/seed/t1/600/400", cat_dict.get("Футболки та топи"), 30),
            ("Сорочка Formal", "Елегантна сорочка для офісу.", 39.99, "https://picsum.photos/seed/t2/600/400", cat_dict.get("Сорочки"), 25),
            ("Куртка Cozy", "Тепла куртка на холодну погоду.", 89.99, "https://picsum.photos/seed/t3/600/400", cat_dict.get("Куртки та пальта"), 15),
            ("Штани Slim", "Стильні вузькі штани.", 49.99, "https://picsum.photos/seed/t4/600/400", cat_dict.get("Штани та джинси"), 40),
            ("Сукня Summer", "Легка літня сукня.", 59.99, "https://picsum.photos/seed/t5/600/400", cat_dict.get("Сукні"), 20),
            ("Кепка Sport", "Кепка для спорту та прогулянок.", 14.99, "https://picsum.photos/seed/t6/600/400", cat_dict.get("Аксесуари"), 50),
        ]
        for title, desc, price, img, cat_id, stock in sample_products:
            with closing(get_conn()) as conn:
                c = conn.cursor()
                c.execute('INSERT INTO products (title, description, price, image_url, category_id, stock) VALUES (?, ?, ?, ?, ?, ?)',
                          (title, desc, price, img, cat_id, stock))
                conn.commit()

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
def create_order(customer_name, customer_email, total, customer_phone=None):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO orders (customer_name, customer_email, customer_phone, total) VALUES (?, ?, ?, ?)',
                  (customer_name, customer_email, customer_phone, total))
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

# Category operations
def add_category(name, description=None):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        return c.lastrowid

def get_categories():
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM categories ORDER BY name')
        return c.fetchall()

def get_category(category_id):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM categories WHERE id=?', (category_id,))
        return c.fetchone()

# Search and filter operations
def search_products(query=None, category_id=None, min_price=None, max_price=None, sort_by='id', sort_order='DESC'):
    # Whitelist allowed sort fields and orders to prevent SQL injection
    allowed_sort_fields = ['id', 'title', 'price', 'rating', 'created_at']
    allowed_sort_orders = ['ASC', 'DESC']
    
    # Validate and sanitize sort parameters
    if sort_by not in allowed_sort_fields:
        sort_by = 'id'
    if sort_order.upper() not in allowed_sort_orders:
        sort_order = 'DESC'
    
    with closing(get_conn()) as conn:
        c = conn.cursor()
        sql = 'SELECT * FROM products WHERE 1=1'
        params = []
        
        if query:
            sql += ' AND (title LIKE ? OR description LIKE ?)'
            params.extend([f'%{query}%', f'%{query}%'])
        
        if category_id:
            sql += ' AND category_id = ?'
            params.append(category_id)
        
        if min_price is not None:
            sql += ' AND price >= ?'
            params.append(min_price)
        
        if max_price is not None:
            sql += ' AND price <= ?'
            params.append(max_price)
        
        sql += f' ORDER BY {sort_by} {sort_order.upper()}'
        
        c.execute(sql, params)
        return c.fetchall()

# Review operations
def add_review(product_id, customer_name, rating, comment):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO reviews (product_id, customer_name, rating, comment) VALUES (?, ?, ?, ?)',
                  (product_id, customer_name, rating, comment))
        conn.commit()
        # Update product rating
        c.execute('SELECT AVG(rating) FROM reviews WHERE product_id=?', (product_id,))
        avg_rating = c.fetchone()[0]
        c.execute('UPDATE products SET rating=? WHERE id=?', (avg_rating, product_id))
        conn.commit()
        return c.lastrowid

def get_reviews(product_id):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM reviews WHERE product_id=? ORDER BY created_at DESC', (product_id,))
        return c.fetchall()

def get_product_rating(product_id):
    with closing(get_conn()) as conn:
        c = conn.cursor()
        c.execute('SELECT AVG(rating), COUNT(*) FROM reviews WHERE product_id=?', (product_id,))
        result = c.fetchone()
        return {'avg_rating': result[0] or 0, 'count': result[1]}
