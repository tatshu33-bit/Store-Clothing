from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import models

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shop')
def shop():
    # Get filter parameters
    query = request.args.get('q', '')
    category_id = request.args.get('category', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'id')
    
    # Get categories for filter
    categories = models.get_categories()
    
    # Search/filter products
    if query or category_id or min_price or max_price:
        products = models.search_products(query, category_id, min_price, max_price, sort_by, 'DESC')
    else:
        products = models.get_products()
    
    return render_template('shop.html', products=products, categories=categories, 
                         current_query=query, current_category=category_id)

@shop_bp.route('/product/<int:pid>')
def product(pid):
    p = models.get_product(pid)
    if not p:
        flash('Товар не знайдено', 'danger')
        return redirect(url_for('shop.shop'))
    
    # Get reviews and rating
    reviews = models.get_reviews(pid)
    rating_info = models.get_product_rating(pid)
    
    return render_template('product.html', product=p, reviews=reviews, rating_info=rating_info)

@shop_bp.route('/product/<int:pid>/review', methods=['POST'])
def add_review(pid):
    name = request.form.get('name', 'Анонім')
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '')
    
    if rating < 1 or rating > 5:
        flash('Рейтинг повинен бути від 1 до 5', 'danger')
        return redirect(url_for('shop.product', pid=pid))
    
    models.add_review(pid, name, rating, comment)
    flash('Відгук додано!', 'success')
    return redirect(url_for('shop.product', pid=pid))

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
        phone = request.form.get('phone', '')
        # calculate total
        total = 0
        for pid, qty in cart.items():
            p = models.get_product(int(pid))
            if p:
                total += p['price'] * qty
        order_id = models.create_order(name, email, total, phone)
        for pid, qty in cart.items():
            p = models.get_product(int(pid))
            if p:
                models.add_order_item(order_id, int(pid), qty, p['price'])
        session['cart'] = {}
        flash(f'Дякуємо! Замовлення №{order_id} успішно створено. Очікуйте дзвінка для підтвердження.', 'success')
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
