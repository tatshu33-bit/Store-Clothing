from flask import Flask, render_template
import models

app = Flask(__name__)
app.secret_key = "replace_this_with_secure_key"
app.config['ADMIN_PASSWORD'] = "adminpass"

# Initialize database
models.init_db()

# Register blueprints
from routes.shop import shop_bp
from routes.admin import admin_bp
from routes.feedback import feedback_bp

app.register_blueprint(shop_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(feedback_bp)

# ---- Main routes ----
@app.route("/")
def index():
    products = models.get_products(limit=3)
    return render_template("index.html", products=products)

# ---- Запуск сервера ----
if __name__ == "__main__":
    app.run(debug=True)

