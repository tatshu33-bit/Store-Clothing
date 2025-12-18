from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "secret"


# Головна сторінка
@app.route("/")
def index():
    products = [
        {
            "id": 1,
            "title": "Футболка",
            "description": "Бавовняна футболка",
            "price": 19.99,
            "image_url": "https://via.placeholder.com/300x200"
        },
        {
            "id": 2,
            "title": "Джинси",
            "description": "Сині джинси",
            "price": 49.99,
            "image_url": "https://via.placeholder.com/300x200"
        },
        {
            "id": 3,
            "title": "Куртка",
            "description": "Тепла зимова куртка",
            "price": 89.99,
            "image_url": "https://via.placeholder.com/300x200"
        }
    ]

    return render_template("index.html", products=products)


# Магазин
@app.route("/shop")
def shop():
    return render_template("shop.html")


# Кошик
@app.route("/cart")
def cart_view():
    return render_template("cart.html")


# Зворотній зв'язок
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


# Адмінка
@app.route("/admin/login")
def admin_login():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)
