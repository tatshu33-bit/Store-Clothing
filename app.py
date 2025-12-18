from flask import Flask, render_template
import models
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'adminpass')
app.config['DATABASE_PATH'] = os.environ.get('DATABASE_PATH', 'db.sqlite')

# Initialize database
models.init_db()

# Register blueprints
from routes.shop import shop_bp
from routes.feedback import feedback_bp
from routes.admin import admin_bp

app.register_blueprint(shop_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')

# ---- Main route ----
@app.route("/")
def index():
    products = models.get_products(limit=3)
    return render_template("index.html", products=products)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# ---- Server startup ----
if __name__ == "__main__":
    # Development mode
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port, debug=debug_mode)

