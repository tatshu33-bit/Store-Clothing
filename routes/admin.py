from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash, session
import models

admin_bp = Blueprint('admin', __name__)

# простий логін (без безпечної автентифікації) для demo
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pwd = request.form.get('password')
        if pwd == current_app.config.get('ADMIN_PASSWORD'):
            session['is_admin'] = True
            return redirect(url_for('admin.dashboard'))
        flash('Невірний пароль', 'danger')
    return render_template('admin_login.html')

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return wrapper

@admin_bp.route('/')
@admin_required
def dashboard():
    feedbacks = models.get_feedbacks()
    orders = models.get_orders()
    products = models.get_products()
    return render_template('admin_dashboard.html', feedbacks=feedbacks, orders=orders, products=products)

@admin_bp.route('/feedback/delete/<int:fid>', methods=['POST'])
@admin_required
def delete_feedback(fid):
    models.delete_feedback(fid)
    flash('Відгук видалено', 'success')
    return redirect(url_for('admin.dashboard'))

# Product management
@admin_bp.route('/products')
@admin_required
def products():
    products = models.get_products()
    return render_template('admin_products.html', products=products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        price = float(request.form.get('price') or 0)
        image = request.form.get('image_url')
        models.add_product(title, desc, price, image)
        flash('Товар додано', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin_product_form.html', product=None)

@admin_bp.route('/products/edit/<int:pid>', methods=['GET', 'POST'])
@admin_required
def edit_product(pid):
    p = models.get_product(pid)
    if not p:
        flash('Товар не знайдено', 'danger')
        return redirect(url_for('admin.products'))
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        price = float(request.form.get('price') or 0)
        image = request.form.get('image_url')
        models.update_product(pid, title, desc, price, image)
        flash('Товар оновлено', 'success')
        return redirect(url_for('admin.products'))
    return render_template('admin_product_form.html', product=p)

@admin_bp.route('/products/delete/<int:pid>', methods=['POST'])
@admin_required
def delete_product(pid):
    models.delete_product(pid)
    flash('Товар видалено', 'success')
    return redirect(url_for('admin.products'))

# Orders
@admin_bp.route('/orders')
@admin_required
def orders():
    orders = models.get_orders()
    return render_template('admin_orders.html', orders=orders)

@admin_bp.route('/orders/<int:oid>')
@admin_required
def order_detail(oid):
    order = models.get_order(oid)
    items = models.get_order_items(oid)
    return render_template('admin_order_detail.html', order=order, items=items)

@admin_bp.route('/orders/<int:oid>/status', methods=['POST'])
@admin_required
def update_status(oid):
    status = request.form.get('status')
    models.update_order_status(oid, status)
    flash('Статус оновлено', 'success')
    return redirect(url_for('admin.order_detail', oid=oid))

@admin_bp.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))
