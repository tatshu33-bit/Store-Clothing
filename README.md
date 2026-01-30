# Магазин одягу (Flask + SQLite)

Простий приклад інтернет-магазину з:
- SQLite БД
- Збереженням відгуків (feedback)
- CRUD для відгуків
- Таблицями товарів та замовлень
- Зв'язками order → order_items → products
- Проста адмін-панель для керування товарами, перегляду/видалення відгуків та управління статусами замовлень
- Comprehensive test suite with 98% code coverage

## Запуск / Setup

1. Встановіть залежності / Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустіть застосунок / Run the application:
   ```bash
   python app.py
   ```

3. Відкрийте / Open: http://127.0.0.1:5000

## Адмін-панель / Admin Panel

- URL: http://127.0.0.1:5000/admin/login
- Пароль за замовчуванням / Default password: `1` (змінити у app.py / change in app.py)

## Тестування / Testing

Проект містить комплексний набір тестів:

### Запуск всіх тестів / Run all tests:
```bash
pytest
```

### Запуск тестів з покриттям коду / Run tests with coverage:
```bash
pytest --cov=. --cov-report=html
```

### Запуск окремих тестів / Run specific tests:
```bash
# Unit tests only
pytest test_models.py

# Integration tests only
pytest test_integration.py
```

### Результати тестування / Test Results:
- **58+ tests** covering all critical functionality
- **98% code coverage**
- Tests include:
  - Unit tests for database operations
  - Integration tests for API endpoints
  - Edge case handling
  - Authentication and authorization
  - Cart and checkout flows

Детальна документація тестів доступна у файлі [TEST_PLANS.md](TEST_PLANS.md).

## Структура файлів / File Structure

- `app.py` — стартовий файл / entry point
- `models.py` — робота з БД / database operations (CRUD)
- `routes/` — маршрути для магазину, відгуків та адмін-панелі / routes
- `templates/` — HTML-шаблони (Bootstrap) / HTML templates
- `test_models.py` — unit tests for models
- `test_integration.py` — integration tests for API endpoints
- `TEST_PLANS.md` — comprehensive test documentation
- `pytest.ini` — pytest configuration
- `db.sqlite` — створюється автоматично / created automatically on first run

## CI/CD

Проект налаштований з GitHub Actions для автоматичного запуску тестів при кожному push або pull request.

The project is configured with GitHub Actions to automatically run tests on every push or pull request.
