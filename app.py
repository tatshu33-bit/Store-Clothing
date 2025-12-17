from flask import Flask, session, redirect, url_for
from routes.admin import admin_bp
from routes.feedback import feedback_bp
from routes.shop import shop_bp
from routes.api import api_bp
import models

app = Flask(__name__)
app.secret_key = "replace_this_with_a_secure_key"
app.config['ADMIN_PASSWORD'] = "1"

# ініціалізація БД (створює таблиці при першому запуску)
models.init_db()

# реєстрація blueprint-ів
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(feedback_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(api_bp)

@app.route('/')
def index():
    from flask import render_template
    products = models.get_products(limit=6)
    return render_template('index.html', products=products)

@app.route('/api-interface')
def api_interface():
    from flask import render_template
    return render_template('api_interface.html')

if __name__ == '__main__':
    app.run(debug=True)
