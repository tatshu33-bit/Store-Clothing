# 📖 Технічна документація ClothesShop

## Огляд архітектури

ClothesShop - це веб-додаток на основі Flask з архітектурою MVC (Model-View-Controller), що використовує SQLite для зберігання даних та Jinja2 для рендерингу шаблонів.

## 🏗️ Архітектурні компоненти

### 1. Application Layer (app.py)

**Відповідальність:**
- Ініціалізація Flask додатку
- Конфігурація (змінні середовища, secret key)
- Реєстрація blueprints
- Обробка глобальних помилок (404, 500)
- Запуск сервера

**Ключові функції:**
```python
def index():
    """Головна сторінка з трьома популярними товарами"""
    
@app.errorhandler(404):
    """Обробка помилки 404 - сторінка не знайдена"""
    
@app.errorhandler(500):
    """Обробка помилки 500 - внутрішня помилка сервера"""
```

### 2. Data Layer (models.py)

**Відповідальність:**
- Визначення структури бази даних
- CRUD операції для всіх сутностей
- Ініціалізація бази даних
- Управління з'єднаннями

**База даних:**
- SQLite3 з row_factory для dict-like доступу
- Context manager для автоматичного закриття з'єднань
- Автоматична ініціалізація таблиць

**Основні функції:**

```python
def init_db():
    """Створює таблиці та додає початкові дані"""
    
def get_conn():
    """Повертає з'єднання з БД з row_factory"""
    
# Feedback CRUD
def add_feedback(name, email, message, rating=None, user_id=None)
def get_feedbacks()
def get_feedback(feedback_id)
def update_feedback(feedback_id, ...)
def delete_feedback(feedback_id)

# Products CRUD
def add_product(title, description, price, stock, category, image_url)
def get_products(limit=None)
def get_product(product_id)
def update_product(product_id, ...)
def delete_product(product_id)

# Orders CRUD
def create_order(customer_name, customer_email, total)
def get_orders()
def get_order(order_id)
def update_order_status(order_id, status)

# Order Items
def add_order_item(order_id, product_id, quantity, price)
def get_order_items(order_id)
```

### 3. Route Layers (routes/)

#### 3.1 Shop Blueprint (routes/shop.py)

**Endpoints:**
- `GET /shop` - Каталог товарів
- `GET /product/<id>` - Деталі товару
- `GET /cart` - Перегляд кошика
- `POST /cart/add/<id>` - Додати в кошик
- `POST /cart/remove/<id>` - Видалити з кошика
- `GET /checkout` - Сторінка оформлення
- `POST /checkout` - Створення замовлення

**Кошик:**
- Зберігається в session (Flask session cookie)
- Формат: `{'product_id': quantity}`
- Автоматично очищується після оформлення замовлення

**Алгоритм checkout:**
1. Перевірка непорожнього кошика
2. Розрахунок загальної суми
3. Створення запису в таблиці orders
4. Створення записів в order_items для кожного товару
5. Очищення session кошика
6. Redirect на магазин

#### 3.2 Feedback Blueprint (routes/feedback.py)

**Endpoints:**
- `GET /feedback` - Сторінка відгуків (форма + список)
- `POST /feedback` - Створення відгуку

**Валідація:**
- Message не може бути порожнім
- Rating (якщо надано) конвертується в int з обробкою помилок
- Email опційний
- Name за замовчуванням "Анонім"

#### 3.3 Admin Blueprint (routes/admin.py)

**Endpoints:**

**Автентифікація:**
- `GET /admin/login` - Сторінка входу
- `POST /admin/login` - Обробка входу
- `GET /admin/logout` - Вихід

**Dashboard:**
- `GET /admin/` - Головна панель (feedback, orders, products overview)

**Products:**
- `GET /admin/products` - Список товарів
- `GET /admin/products/add` - Форма додавання
- `POST /admin/products/add` - Створення товару
- `GET /admin/products/edit/<id>` - Форма редагування
- `POST /admin/products/edit/<id>` - Оновлення товару
- `POST /admin/products/delete/<id>` - Видалення товару

**Orders:**
- `GET /admin/orders` - Список замовлень
- `GET /admin/orders/<id>` - Деталі замовлення
- `POST /admin/orders/<id>/status` - Оновлення статусу

**Feedback:**
- `POST /admin/feedback/delete/<id>` - Видалення відгуку

**Безпека:**
- Декоратор `@admin_required` перевіряє `session['is_admin']`
- Пароль зберігається в `app.config['ADMIN_PASSWORD']`
- Session-based автентифікація

### 4. View Layer (templates/)

**Базовий шаблон (base.html):**
- Bootstrap 5 для стилізації
- Навігаційна панель
- Flash messages
- Content block для дочірніх шаблонів

**Структура наслідування:**
```
base.html
├── index.html (головна)
├── shop.html (каталог)
├── product.html (деталі товару)
├── cart.html (кошик)
├── checkout.html (оформлення)
├── feedback.html (відгуки)
├── admin_login.html (вхід адміна)
├── admin_dashboard.html (панель)
├── admin_products.html (список товарів)
├── admin_product_form.html (форма товару)
├── admin_orders.html (список замовлень)
├── admin_order_detail.html (деталі замовлення)
├── 404.html (помилка 404)
└── 500.html (помилка 500)
```

## 🗄️ Схема бази даних

### ER діаграма:

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│  products   │       │ order_items  │       │   orders    │
├─────────────┤       ├──────────────┤       ├─────────────┤
│ id (PK)     │◄──────│ product_id   │       │ id (PK)     │
│ title       │       │ order_id     │──────►│ customer_*  │
│ description │       │ quantity     │       │ status      │
│ price       │       │ price        │       │ total       │
│ stock       │       └──────────────┘       │ created_at  │
│ category    │                              └─────────────┘
│ image_url   │
└─────────────┘

┌─────────────┐
│  feedback   │
├─────────────┤
│ id (PK)     │
│ user_id     │
│ name        │
│ email       │
│ message     │
│ rating      │
│ created_at  │
└─────────────┘
```

### Індекси:

База даних використовує стандартні PRIMARY KEY індекси. Для оптимізації можна додати:

```sql
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

## 🔄 Потік даних

### Процес оформлення замовлення:

```
User Action → Flask Route → Business Logic → Database → Response
    │              │               │              │          │
[Add to cart] → [cart_add()] → [session.update] → (N/A) → [Redirect]
    │              │               │              │          │
[Checkout]    → [checkout()]  → [calculate]   → [INSERT] → [Confirm]
```

**Детально:**

1. **Користувач додає товар:**
   - POST /cart/add/1 з quantity=2
   - `cart_add()` оновлює session
   - Redirect на /cart

2. **Перегляд кошика:**
   - GET /cart
   - `cart_view()` читає з session
   - Запитує products з БД
   - Рендерить cart.html

3. **Оформлення:**
   - POST /checkout з name, email
   - `checkout()`:
     - Рахує total
     - `create_order()` → INSERT в orders
     - Loop: `add_order_item()` → INSERT в order_items
     - Очищає session['cart']
   - Redirect на /shop

### Процес управління товарами (Admin):

```
Admin Login → Dashboard → Product Management → CRUD Operations
     │            │              │                    │
[Authenticate] → [View All] → [Select Action] → [Update DB]
     │            │              │                    │
[session set] → [get_products()] → [form submit] → [SQL UPDATE]
```

## 🔐 Безпека

### Поточні механізми:

1. **Session-based auth:**
   - Flask sessions (signed cookies)
   - `is_admin` flag в session

2. **SQL Injection Protection:**
   - Параметризовані запити (sqlite3 placeholders)
   - Приклад: `c.execute('SELECT * FROM products WHERE id=?', (pid,))`

3. **Input Validation:**
   - Try-except для конвертації типів
   - Required fields validation
   - Rating CHECK constraint (1-5)

4. **CSRF Protection:**
   - ⚠️ Потребує додавання Flask-WTF

### Рекомендації для покращення:

1. **Додати CSRF токени:**
```python
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

2. **Password hashing для адміна:**
```python
from werkzeug.security import generate_password_hash, check_password_hash
```

3. **Rate limiting:**
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
```

4. **HTTPS Only cookies:**
```python
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

## 📊 Продуктивність

### Поточна оптимізація:

- ✅ Context managers для auto-close connections
- ✅ Row factory для dict-like access
- ✅ Обмеження LIMIT для запитів (наприклад, index показує 3 товари)

### Можливі покращення:

1. **Кешування:**
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=300)
def get_products():
    # ...
```

2. **Pagination:**
```python
def get_products(page=1, per_page=12):
    offset = (page - 1) * per_page
    # ... LIMIT per_page OFFSET offset
```

3. **Eager loading (для JOIN запитів):**
```sql
SELECT oi.*, p.title, p.image_url 
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.id
WHERE oi.order_id = ?
```

4. **Connection pooling:**
```python
from flask_sqlalchemy import SQLAlchemy
# Migrate to SQLAlchemy for connection pooling
```

## 🧪 Тестування

### Структура тестів (рекомендовано):

```
tests/
├── test_models.py      # Тести моделей та БД
├── test_routes.py      # Тести endpoints
├── test_cart.py        # Тести кошика
└── conftest.py         # Fixtures
```

### Приклад тесту:

```python
import pytest
from app import app
import models

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'ClothesShop' in rv.data

def test_add_product_to_cart(client):
    rv = client.post('/cart/add/1', data={'quantity': 2})
    assert rv.status_code == 302  # Redirect
```

## 🔧 Конфігурація

### Змінні середовища:

| Змінна | Опис | Значення за замовчуванням |
|--------|------|---------------------------|
| FLASK_ENV | Режим роботи | development |
| SECRET_KEY | Секретний ключ для sessions | dev-secret-key-change-in-production |
| ADMIN_PASSWORD | Пароль адміністратора | adminpass |
| DATABASE_PATH | Шлях до БД | db.sqlite |
| HOST | Хост для прослуховування | 127.0.0.1 |
| PORT | Порт сервера | 5000 |

### Конфігурація для різних середовищ:

**Development:**
```bash
export FLASK_ENV=development
export SECRET_KEY=dev-key
python app.py
```

**Production:**
```bash
export FLASK_ENV=production
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
gunicorn --bind 0.0.0.0:5000 app:app
```

## 📈 Масштабування

### Вертикальне масштабування:

1. **Збільшення workers (Gunicorn):**
```bash
gunicorn --workers 4 --threads 2 app:app
```

2. **Оптимізація БД:**
   - Індекси на часто використовуваних полях
   - Міграція на PostgreSQL для concurrent writes

### Горизонтальне масштабування:

1. **Load Balancer** (Nginx/HAProxy)
2. **Distributed Sessions** (Redis)
3. **Централізована БД** (PostgreSQL/MySQL)
4. **CDN** для статичних файлів

## 📚 API Reference

Детальний опис всіх endpoints дивіться в [README.md](README.md#-api-маршрути)

## 🔄 Життєвий цикл запиту

```
Client Request
    ↓
Nginx/Load Balancer (optional)
    ↓
Gunicorn Worker
    ↓
Flask Application
    ↓
Route Handler (Blueprint)
    ↓
Business Logic
    ↓
Database Query (models.py)
    ↓
Template Rendering (Jinja2)
    ↓
HTTP Response
    ↓
Client
```

---

**Документація оновлена:** 2024-12-18
