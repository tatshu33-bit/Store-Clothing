from flask import Flask, render_template, session, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = "replace_this_with_secure_key"

# ---- Дані (імітація БД) ----
products_data = [
    {"id": 1, "title": "Футболка", "description": "Бавовняна футболка", "price": 19.99},
    {"id": 2, "title": "Джинси", "description": "Сині джинси", "price": 49.99},
    {"id": 3, "title": "Куртка", "description": "Тепла зимова куртка", "price": 89.99},
]

feedbacks = []  # список відгуків
ADMIN_PASSWORD = "1"

# ---- Допоміжні функції ----
def _cart():
    return session.setdefault('cart', {})

def get_product(pid):
    for p in products_data:
        if p["id"] == pid:
            return p
    return None

# ---- Маршрути ----
@app.route("/")
def index():
    return render_template("index.html", products=products_data[:3])

@app.route("/shop")
def shop():
    return render_template("shop.html", products=products_data)

@app.route("/product/<int:pid>")
def product(pid):
    p = get_product(pid)
    if not p:
        return "Товар не знайдено", 404
    return render_template("product.html", product=p)

@app.route("/cart")
def cart_view():
    cart = _cart()
    items = []
    total = 0
    for pid, qty in cart.items():
        p = get_product(int(pid))
        if p:
            subtotal = p["price"] * qty
            items.append({"product": p, "qty": qty, "subtotal": subtotal})
            total += subtotal
    return render_template("cart.html", items=items, total=total)

@app.route("/cart/add/<int:pid>", methods=["POST"])
def cart_add(pid):
    qty = int(request.form.get("quantity", 1))
    cart = _cart()
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session['cart'] = cart
    flash("Додано до кошика", "success")
    return redirect(url_for("cart_view"))

@app.route("/cart/remove/<int:pid>", methods=["POST"])
def cart_remove(pid):
    cart = _cart()
    cart.pop(str(pid), None)
    session['cart'] = cart
    flash("Видалено з кошика", "success")
    return redirect(url_for("cart_view"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart = _cart()
    if not cart:
        flash("Кошик порожній", "warning")
        return redirect(url_for("shop"))

    if request.method == "POST":
        name = request.form.get("name") or "Клієнт"
        email = request.form.get("email")
        flash(f"Дякуємо, {name}! Замовлення оформлено.", "success")
        session['cart'] = {}
        return redirect(url_for("shop"))

    items = []
    total = 0
    for pid, qty in cart.items():
        p = get_product(int(pid))
        if p:
            subtotal = p["price"] * qty
            items.append({"product": p, "qty": qty, "subtotal": subtotal})
            total += subtotal
    return render_template("checkout.html", items=items, total=total)

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name") or "Анонім"
        email = request.form.get("email")
        message = request.form.get("message")
        feedbacks.append({"name": name, "email": email, "message": message})
        flash("Відгук надіслано!", "success")
        return redirect(url_for("feedback"))
    return render_template("feedback.html", feedbacks=feedbacks)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            flash("Ви увійшли як адміністратор", "success")
            return redirect(url_for("shop"))
        else:
            flash("Невірний пароль", "danger")
    return render_template("admin.html")

# ---- Запуск сервера ----
if __name__ == "__main__":
    app.run(debug=True)

