from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/cart")
def cart_view():
    return render_template("cart.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/admin/login")
def admin_login():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
