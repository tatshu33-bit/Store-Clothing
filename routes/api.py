from flask import Blueprint, request, jsonify
import models

api_bp = Blueprint('api', __name__)

# Products API
@api_bp.route('/api/products', methods=['GET'])
def get_products_api():
    """Get all products as JSON"""
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
        return jsonify({'success': True, 'products': products_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/api/products', methods=['POST'])
def add_product_api():
    """Add a new product via JSON"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        title = data.get('title')
        description = data.get('description', '')
        price = data.get('price')
        image_url = data.get('image_url', '')
        
        if not title:
            return jsonify({'success': False, 'error': 'Title is required'}), 400
        if not price:
            return jsonify({'success': False, 'error': 'Price is required'}), 400
        
        try:
            price = float(price)
        except ValueError:
            return jsonify({'success': False, 'error': 'Price must be a number'}), 400
        
        product_id = models.add_product(title, description, price, image_url)
        return jsonify({
            'success': True,
            'message': 'Product added successfully',
            'product_id': product_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Feedback API
@api_bp.route('/api/feedback', methods=['GET'])
def get_feedback_api():
    """Get all feedback as JSON"""
    try:
        feedbacks = models.get_feedbacks()
        feedback_list = []
        for f in feedbacks:
            feedback_list.append({
                'id': f['id'],
                'name': f['name'],
                'email': f['email'],
                'message': f['message'],
                'created_at': f['created_at']
            })
        return jsonify({'success': True, 'feedback': feedback_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/api/feedback', methods=['POST'])
def add_feedback_api():
    """Add new feedback via JSON"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        name = data.get('name', 'Anonymous')
        email = data.get('email', '')
        message = data.get('message')
        
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400
        
        feedback_id = models.add_feedback(name, email, message)
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully',
            'feedback_id': feedback_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
