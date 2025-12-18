from flask import Flask, session, redirect, url_for, render_template
from flask_wtf.csrf import CSRFProtect
from routes.admin import admin_bp
from routes.feedback import feedback_bp
from routes.shop import shop_bp
import models
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24).hex())
app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD', "adminpass")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['WTF_CSRF_TIME_LIMIT'] = None  # CSRF tokens don't expire

# Enable CSRF protection
csrf = CSRFProtect(app)

# ініціалізація БД (створює таблиці при першому запуску)
models.init_db()

# реєстрація blueprint-ів
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(feedback_bp)
app.register_blueprint(shop_bp)

@app.route('/')
def index():
    products = models.get_products(limit=6)
    return render_template('index.html', products=products)

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error_code=404, error_message="Сторінка не знайдена"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error_code=500, error_message="Внутрішня помилка сервера"), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', error_code=403, error_message="Доступ заборонено"), 403

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
