from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import models

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shop')
def shop():
    products = models.get_products()
    return render_template('shop.html', products=products)

@shop_bp.route('/product/<int:pid>')
def product(pid):
    p = models.get_product(pid)
    if not p:
        return "Товар не знайдено", 404
    return render_template('product.html', product=p)

# cart stored in session as {'product_id': qty}
def _cart():
    return session.setdefault('cart', {})

@shop_bp.route('/cart')
def cart_view():
    cart = _cart()
    items = []
    total = 0
    for pid, qty in cart.items():
        p = models.get_product(int(pid))
        if not p:
            continue
        subtotal = p['price'] * qty
        items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
        total += subtotal
    return render_template('cart.html', items=items, total=total)

@shop_bp.route('/cart/add/<int:pid>', methods=['POST'])
def cart_add(pid):
    qty = int(request.form.get('quantity', 1))
    cart = _cart()
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session['cart'] = cart
    flash('Додано до кошика', 'success')
    return redirect(url_for('shop.cart_view'))

@shop_bp.route('/cart/remove/<int:pid>', methods=['POST'])
def cart_remove(pid):
    cart = _cart()
    cart.pop(str(pid), None)
    session['cart'] = cart
    flash('Видалено з кошика', 'success')
    return redirect(url_for('shop.cart_view'))

@shop_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = _cart()
    if not cart:
        flash('Кошик порожній', 'warning')
        return redirect(url_for('shop.shop'))
    if request.method == 'POST':
        name = request.form.get('name') or 'Клієнт'
        email = request.form.get('email')
        # calculate total
        total = 0
        for pid, qty in cart.items():
            p = models.get_product(int(pid))
            if p:
                total += p['price'] * qty
        order_id = models.create_order(name, email, total)
        for pid, qty in cart.items():
            p = models.get_product(int(pid))
            if p:
                models.add_order_item(order_id, int(pid), qty, p['price'])
        session['cart'] = {}
        flash(f'Дякуємо! Замовлення {order_id} створено.', 'success')
        return redirect(url_for('shop.shop'))
    # GET
    items = []
    total = 0
    for pid, qty in cart.items():
        p = models.get_product(int(pid))
        if not p:
            continue
        subtotal = p['price'] * qty
        items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
        total += subtotal
    return render_template('checkout.html', items=items, total=total)
