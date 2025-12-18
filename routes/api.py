from flask import Blueprint, jsonify, request
import models

api_bp = Blueprint('api', __name__)

# Error handlers
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@api_bp.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

# Products endpoints
@api_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products = models.get_products()
        products_list = []
        for p in products:
            products_list.append({
                'id': p['id'],
                'title': p['title'],
                'description': p['description'],
                'price': p['price'],
                'image_url': p['image_url']
            })
        return jsonify({'products': products_list, 'count': len(products_list)}), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@api_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    try:
        product = models.get_product(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({
            'id': product['id'],
            'title': product['title'],
            'description': product['description'],
            'price': product['price'],
            'image_url': product['image_url']
        }), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@api_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'title' not in data or 'price' not in data:
            return jsonify({'error': 'Missing required fields: title and price'}), 400
        
        title = data.get('title')
        description = data.get('description', '')
        price = data.get('price')
        image_url = data.get('image_url', None)
        
        # Validate price
        try:
            price = float(price)
            if price < 0:
                return jsonify({'error': 'Price must be a positive number'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid price format'}), 400
        
        product_id = models.add_product(title, description, price, image_url)
        
        return jsonify({
            'message': 'Product created successfully',
            'id': product_id,
            'product': {
                'id': product_id,
                'title': title,
                'description': description,
                'price': price,
                'image_url': image_url
            }
        }), 201
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@api_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product"""
    try:
        # Check if product exists
        product = models.get_product(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Use existing values if not provided
        title = data.get('title', product['title'])
        description = data.get('description', product['description'])
        price = data.get('price', product['price'])
        image_url = data.get('image_url', product['image_url'])
        
        # Validate price if provided
        try:
            price = float(price)
            if price < 0:
                return jsonify({'error': 'Price must be a positive number'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid price format'}), 400
        
        models.update_product(product_id, title, description, price, image_url)
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': {
                'id': product_id,
                'title': title,
                'description': description,
                'price': price,
                'image_url': image_url
            }
        }), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@api_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    try:
        # Check if product exists
        product = models.get_product(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        models.delete_product(product_id)
        
        return jsonify({
            'message': 'Product deleted successfully',
            'id': product_id
        }), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# Orders endpoints
@api_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        orders = models.get_orders()
        orders_list = []
        for o in orders:
            orders_list.append({
                'id': o['id'],
                'customer_name': o['customer_name'],
                'customer_email': o['customer_email'],
                'status': o['status'],
                'total': o['total'],
                'created_at': o['created_at']
            })
        return jsonify({'orders': orders_list, 'count': len(orders_list)}), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@api_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a single order by ID with items"""
    try:
        order = models.get_order(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Get order items
        items = models.get_order_items(order_id)
        items_list = []
        for item in items:
            items_list.append({
                'id': item['id'],
                'product_id': item['product_id'],
                'product_title': item['title'],
                'quantity': item['quantity'],
                'price': item['price']
            })
        
        return jsonify({
            'id': order['id'],
            'customer_name': order['customer_name'],
            'customer_email': order['customer_email'],
            'status': order['status'],
            'total': order['total'],
            'created_at': order['created_at'],
            'items': items_list
        }), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@api_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'customer_name' not in data or 'items' not in data:
            return jsonify({'error': 'Missing required fields: customer_name and items'}), 400
        
        customer_name = data.get('customer_name')
        customer_email = data.get('customer_email', '')
        items = data.get('items', [])
        
        if not items or not isinstance(items, list):
            return jsonify({'error': 'Items must be a non-empty list'}), 400
        
        # Calculate total and validate items
        total = 0
        validated_items = []
        for item in items:
            if 'product_id' not in item or 'quantity' not in item:
                return jsonify({'error': 'Each item must have product_id and quantity'}), 400
            
            product = models.get_product(item['product_id'])
            if not product:
                return jsonify({'error': f'Product {item["product_id"]} not found'}), 404
            
            try:
                quantity = int(item['quantity'])
            except (ValueError, TypeError):
                return jsonify({'error': 'Quantity must be a valid integer'}), 400
            
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be greater than 0'}), 400
            
            total += product['price'] * quantity
            validated_items.append({
                'product_id': item['product_id'],
                'quantity': quantity,
                'price': product['price']
            })
        
        # Create order
        order_id = models.create_order(customer_name, customer_email, total)
        
        # Add order items using validated data
        for item in validated_items:
            models.add_order_item(order_id, item['product_id'], item['quantity'], item['price'])
        
        return jsonify({
            'message': 'Order created successfully',
            'id': order_id,
            'order': {
                'id': order_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'total': total,
                'status': 'new'
            }
        }), 201
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500
