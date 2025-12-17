from flask import Flask, session, redirect, url_for, jsonify
from routes.admin import admin_bp
from routes.feedback import feedback_bp
from routes.shop import shop_bp
import models
import os

app = Flask(__name__)
# Use environment variable for secret key with fallback
app.secret_key = os.environ.get('SECRET_KEY', 'replace_this_with_a_secure_key')
# Use environment variable for admin password with fallback
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', '1')

# ініціалізація БД (створює таблиці при першому запуску)
models.init_db()

# реєстрація blueprint-ів
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(feedback_bp)
app.register_blueprint(shop_bp)

@app.route('/')
def index():
    from flask import render_template
    products = models.get_products(limit=6)
    return render_template('index.html', products=products)

@app.route('/health')
def health():
    """Health check endpoint for container monitoring"""
    try:
        # Check database connectivity
        models.get_products(limit=1)
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

if __name__ == '__main__':
    app.run(debug=True)
