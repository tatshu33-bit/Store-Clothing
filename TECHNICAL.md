# Технічна документація Store-Clothing

## Огляд системи

Store-Clothing - це веб-застосунок для інтернет-магазину одягу, розроблений на Flask з використанням SQLite як бази даних. Система надає функціональність для перегляду каталогу товарів, управління кошиком, оформлення замовлень та адміністративну панель для керування магазином.

## Архітектура

### Стек технологій

- **Backend Framework**: Flask 3.0.0
- **База даних**: SQLite
- **Frontend**: Bootstrap 5.3.1, Bootstrap Icons
- **Безпека**: Flask-WTF (CSRF Protection)
- **Конфігурація**: python-dotenv

### Структура проєкту

```
Store-Clothing/
├── app.py                 # Головний файл застосунку
├── models.py              # Моделі даних та взаємодія з БД
├── requirements.txt       # Залежності Python
├── .env.example          # Приклад конфігурації
├── routes/               # Blueprint-и маршрутів
│   ├── admin.py         # Адміністративна панель
│   ├── feedback.py      # Зворотній зв'язок
│   └── shop.py          # Магазин та кошик
└── templates/           # HTML шаблони
    ├── base.html        # Базовий шаблон
    ├── index.html       # Головна сторінка
    ├── shop.html        # Каталог товарів
    ├── product.html     # Сторінка товару
    ├── cart.html        # Кошик
    ├── checkout.html    # Оформлення замовлення
    ├── feedback.html    # Зворотній зв'язок
    └── admin_*.html     # Адмін панель
```

## База даних

### Схема БД

#### Таблиця `categories`
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
)
```

#### Таблиця `products`
```sql
CREATE TABLE products (
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
```

#### Таблиця `orders`
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    customer_email TEXT,
    customer_phone TEXT,
    status TEXT DEFAULT 'new',
    total REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Таблиця `order_items`
```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
```

#### Таблиця `reviews`
```sql
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    customer_name TEXT,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id)
)
```

#### Таблиця `feedback`
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
)
```

## API та Маршрути

### Публічні маршрути

#### Головна сторінка
- **URL**: `/`
- **Метод**: GET
- **Опис**: Відображає головну сторінку з популярними товарами

#### Каталог
- **URL**: `/shop`
- **Метод**: GET
- **Параметри**:
  - `q` (str): Пошуковий запит
  - `category` (int): ID категорії
  - `min_price` (float): Мінімальна ціна
  - `max_price` (float): Максимальна ціна
  - `sort` (str): Поле для сортування
- **Опис**: Відображає каталог товарів з фільтрами та пошуком

#### Сторінка товару
- **URL**: `/product/<int:pid>`
- **Метод**: GET
- **Опис**: Детальна інформація про товар, відгуки, рейтинг

#### Додати відгук
- **URL**: `/product/<int:pid>/review`
- **Метод**: POST
- **Параметри**:
  - `name` (str): Ім'я користувача
  - `rating` (int): Рейтинг 1-5
  - `comment` (str): Текст відгуку
- **Опис**: Додає відгук до товару

#### Кошик
- **URL**: `/cart`
- **Метод**: GET
- **Опис**: Відображає вміст кошика

#### Додати до кошика
- **URL**: `/cart/add/<int:pid>`
- **Метод**: POST
- **Параметри**:
  - `quantity` (int): Кількість товару
- **Опис**: Додає товар до кошика

#### Видалити з кошика
- **URL**: `/cart/remove/<int:pid>`
- **Метод**: POST
- **Опис**: Видаляє товар з кошика

#### Оформлення замовлення
- **URL**: `/checkout`
- **Метод**: GET, POST
- **Параметри** (POST):
  - `name` (str): Ім'я клієнта
  - `email` (str): Email клієнта
  - `phone` (str): Телефон клієнта
- **Опис**: Оформлення замовлення

#### Зворотній зв'язок
- **URL**: `/feedback`
- **Метод**: GET, POST
- **Параметри** (POST):
  - `name` (str): Ім'я
  - `email` (str): Email
  - `message` (str): Повідомлення
- **Опис**: Форма зворотного зв'язку

### Адміністративні маршрути

Всі адміністративні маршрути захищені декоратором `@admin_required` та доступні тільки після авторизації.

#### Вхід до адмін-панелі
- **URL**: `/admin/login`
- **Метод**: GET, POST
- **Опис**: Авторизація адміністратора

#### Dashboard
- **URL**: `/admin/`
- **Метод**: GET
- **Опис**: Головна панель адміністратора

#### Управління товарами
- **URL**: `/admin/products`
- **Метод**: GET
- **Опис**: Список товарів

- **URL**: `/admin/products/add`
- **Метод**: GET, POST
- **Опис**: Додавання нового товару

- **URL**: `/admin/products/edit/<int:pid>`
- **Метод**: GET, POST
- **Опис**: Редагування товару

- **URL**: `/admin/products/delete/<int:pid>`
- **Метод**: POST
- **Опис**: Видалення товару

#### Управління замовленнями
- **URL**: `/admin/orders`
- **Метод**: GET
- **Опис**: Список замовлень

- **URL**: `/admin/orders/<int:oid>`
- **Метод**: GET
- **Опис**: Деталі замовлення

- **URL**: `/admin/orders/<int:oid>/status`
- **Метод**: POST
- **Опис**: Оновлення статусу замовлення

## Безпека

### Захист від загроз

1. **CSRF Protection**: Використовується Flask-WTF для захисту від CSRF атак
2. **SQL Injection**: Використання параметризованих запитів
3. **XSS**: Автоматичне екранування в Jinja2 шаблонах
4. **Session Security**: Безпечний секретний ключ через змінні середовища
5. **Password Storage**: Пароль адміністратора зберігається в .env файлі

### Конфігурація безпеки

```python
# app.py
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24).hex())
app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD', "adminpass")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
csrf = CSRFProtect(app)
```

## Встановлення та запуск

### Вимоги
- Python 3.8+
- pip

### Встановлення

1. Клонування репозиторію:
```bash
git clone https://github.com/yourusername/Store-Clothing.git
cd Store-Clothing
```

2. Створення віртуального середовища:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate  # Windows
```

3. Встановлення залежностей:
```bash
pip install -r requirements.txt
```

4. Налаштування змінних середовища:
```bash
cp .env.example .env
# Відредагуйте .env файл з вашими налаштуваннями
```

5. Запуск застосунку:
```bash
python app.py
```

Застосунок буде доступний за адресою: http://127.0.0.1:5000

## Розгортання в Production

### Рекомендації для production

1. **Використовуйте WSGI сервер** (Gunicorn, uWSGI):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

2. **Налаштуйте reverse proxy** (Nginx, Apache)

3. **Використовуйте PostgreSQL** замість SQLite для кращої продуктивності

4. **Увімкніть HTTPS** з SSL сертифікатом

5. **Налаштуйте логування**:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

6. **Вимкніть DEBUG режим**:
```bash
# .env
FLASK_DEBUG=False
FLASK_ENV=production
```

7. **Додайте monitoring та error tracking** (Sentry, CloudWatch)

### Змінні середовища для production

```bash
SECRET_KEY=your-very-secure-random-key-here
ADMIN_PASSWORD=strong-admin-password
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_PATH=/path/to/production/db.sqlite
```

## Оптимізація

### Рекомендації з продуктивності

1. **Індекси БД**: Додайте індекси для часто використовуваних полів:
```sql
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_rating ON products(rating);
CREATE INDEX idx_orders_status ON orders(status);
```

2. **Кешування**: Використовуйте Flask-Caching для кешування:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=300)
def get_popular_products():
    return models.get_products(limit=6)
```

3. **CDN**: Використовуйте CDN для статичних ресурсів

4. **Compression**: Увімкніть gzip стиснення

5. **Database Connection Pooling**: Використовуйте пул з'єднань для БД

## Тестування

### Рекомендації для тестування

1. **Unit тести**: Тестування моделей та функцій
```python
import unittest
from models import add_product, get_product

class TestModels(unittest.TestCase):
    def test_add_product(self):
        pid = add_product("Test", "Description", 10.0, None)
        self.assertIsNotNone(pid)
```

2. **Integration тести**: Тестування маршрутів
```python
def test_shop_route(self):
    with app.test_client() as client:
        response = client.get('/shop')
        self.assertEqual(response.status_code, 200)
```

3. **E2E тести**: Selenium для тестування UI

## Підтримка

### Логування

Логи зберігаються в консолі. Для production рекомендується налаштувати запис у файли:

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
```

### Моніторинг

Рекомендовані інструменти:
- Prometheus + Grafana для метрик
- Sentry для відстеження помилок
- ELK Stack для аналізу логів

## Ліцензія

MIT License

## Контакти

Для питань та пропозицій: info@clothesshop.ua
