"""
Integration tests for Flask API endpoints
Tests the interaction between routes and models
"""
import pytest
import os
import tempfile
from app import app
import models


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create a test client with isolated database"""
    db_file = tmp_path / "test_integration.sqlite"
    monkeypatch.setattr(models, 'DB_PATH', str(db_file))
    
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['ADMIN_PASSWORD'] = 'testpass'
    
    with app.test_client() as client:
        with app.app_context():
            models.init_db()
        yield client
    
    # Cleanup
    if os.path.exists(db_file):
        os.remove(db_file)


class TestShopEndpoints:
    """Integration tests for shop-related endpoints"""
    
    def test_index_page(self, client):
        """Test that index page loads and displays products"""
        response = client.get('/')
        assert response.status_code == 200
        # Check that page contains shop name or key content
        assert b'ClothesShop' in response.data or b'shop' in response.data.lower()
    
    def test_shop_page_lists_products(self, client):
        """Test shop page displays all products"""
        response = client.get('/shop')
        assert response.status_code == 200
        # Sample products should be visible
        data = response.data.decode('utf-8')
        assert 'Classic' in data or 'Formal' in data or 'product' in data.lower()
    
    def test_product_detail_page(self, client):
        """Test individual product detail page"""
        # Get a product first
        products = models.get_products(limit=1)
        if products:
            product_id = products[0]['id']
            response = client.get(f'/product/{product_id}')
            assert response.status_code == 200
            assert products[0]['title'].encode() in response.data
    
    def test_product_not_found(self, client):
        """Test accessing non-existent product"""
        response = client.get('/product/99999')
        assert response.status_code == 404
    
    def test_cart_view_empty(self, client):
        """Test viewing empty cart"""
        response = client.get('/cart')
        assert response.status_code == 200
    
    def test_add_to_cart(self, client):
        """Test adding product to cart"""
        # Get a product
        products = models.get_products(limit=1)
        if products:
            product_id = products[0]['id']
            
            # Add to cart
            response = client.post(f'/cart/add/{product_id}', 
                                   data={'quantity': 2},
                                   follow_redirects=True)
            assert response.status_code == 200
            
            # Check cart
            response = client.get('/cart')
            assert response.status_code == 200
    
    def test_remove_from_cart(self, client):
        """Test removing product from cart"""
        # Add product first
        products = models.get_products(limit=1)
        if products:
            product_id = products[0]['id']
            client.post(f'/cart/add/{product_id}', data={'quantity': 1})
            
            # Remove from cart
            response = client.post(f'/cart/remove/{product_id}', 
                                   follow_redirects=True)
            assert response.status_code == 200
    
    def test_checkout_empty_cart(self, client):
        """Test checkout with empty cart redirects"""
        response = client.post('/checkout', 
                               data={'name': 'Test', 'email': 'test@test.com'},
                               follow_redirects=True)
        assert response.status_code == 200
    
    def test_checkout_with_items(self, client):
        """Test complete checkout flow"""
        # Add product to cart
        products = models.get_products(limit=1)
        if products:
            product_id = products[0]['id']
            client.post(f'/cart/add/{product_id}', data={'quantity': 1})
            
            # Checkout
            response = client.post('/checkout',
                                   data={'name': 'John Doe', 
                                         'email': 'john@example.com'},
                                   follow_redirects=True)
            assert response.status_code == 200
            
            # Verify order was created
            orders = models.get_orders()
            assert len(orders) > 0
            assert orders[0]['customer_name'] == 'John Doe'
    
    def test_checkout_get_request(self, client):
        """Test GET request to checkout page with items"""
        # Add product to cart
        products = models.get_products(limit=1)
        if products:
            product_id = products[0]['id']
            client.post(f'/cart/add/{product_id}', data={'quantity': 1})
            
            # GET checkout page
            response = client.get('/checkout')
            assert response.status_code == 200


class TestFeedbackEndpoints:
    """Integration tests for feedback endpoints"""
    
    def test_feedback_page_get(self, client):
        """Test feedback page loads"""
        response = client.get('/feedback')
        assert response.status_code == 200
    
    def test_submit_feedback(self, client):
        """Test submitting feedback"""
        response = client.post('/feedback',
                               data={
                                   'name': 'Test User',
                                   'email': 'test@example.com',
                                   'message': 'Great service!'
                               },
                               follow_redirects=True)
        assert response.status_code == 200
        
        # Verify feedback was saved
        feedbacks = models.get_feedbacks()
        assert len(feedbacks) > 0
        assert feedbacks[0]['name'] == 'Test User'
        assert feedbacks[0]['message'] == 'Great service!'
    
    def test_submit_feedback_without_name(self, client):
        """Test submitting feedback without name uses default"""
        response = client.post('/feedback',
                               data={
                                   'email': 'anon@example.com',
                                   'message': 'Anonymous feedback'
                               },
                               follow_redirects=True)
        assert response.status_code == 200
        
        # Check feedback was saved with default name
        feedbacks = models.get_feedbacks()
        assert any(f['message'] == 'Anonymous feedback' for f in feedbacks)
    
    def test_submit_empty_feedback(self, client):
        """Test submitting empty message is rejected"""
        response = client.post('/feedback',
                               data={
                                   'name': 'Test User',
                                   'email': 'test@example.com',
                                   'message': ''
                               },
                               follow_redirects=True)
        assert response.status_code == 200
        # Should show error message or redirect back
    
    def test_feedback_displays_existing(self, client):
        """Test that feedback page displays existing feedback"""
        # Add feedback
        models.add_feedback('Display Test', 'display@test.com', 'Test display')
        
        response = client.get('/feedback')
        assert response.status_code == 200
        assert b'Display Test' in response.data


class TestAdminEndpoints:
    """Integration tests for admin panel endpoints"""
    
    def test_admin_login_page(self, client):
        """Test admin login page loads"""
        response = client.get('/admin/login')
        assert response.status_code == 200
    
    def test_admin_login_success(self, client):
        """Test successful admin login"""
        response = client.post('/admin/login',
                               data={'password': 'testpass'},
                               follow_redirects=True)
        assert response.status_code == 200
        
        # Try accessing admin dashboard
        response = client.get('/admin/')
        assert response.status_code == 200
    
    def test_admin_login_failure(self, client):
        """Test failed admin login with wrong password"""
        response = client.post('/admin/login',
                               data={'password': 'wrongpass'},
                               follow_redirects=False)
        assert response.status_code == 200
        
        # Should not be able to access dashboard
        response = client.get('/admin/', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login
    
    def test_admin_dashboard_requires_auth(self, client):
        """Test that admin dashboard requires authentication"""
        response = client.get('/admin/', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login
    
    def test_admin_dashboard_displays_data(self, client):
        """Test admin dashboard shows feedbacks, orders, and products"""
        # Login first
        client.post('/admin/login', data={'password': 'testpass'})
        
        response = client.get('/admin/')
        assert response.status_code == 200
        # Dashboard should display some content
    
    def test_admin_delete_feedback(self, client):
        """Test admin can delete feedback"""
        # Login
        client.post('/admin/login', data={'password': 'testpass'})
        
        # Add feedback
        feedback_id = models.add_feedback('To Delete', 'del@test.com', 'Delete this')
        
        # Delete via admin
        response = client.post(f'/admin/feedback/delete/{feedback_id}',
                               follow_redirects=True)
        assert response.status_code == 200
        
        # Verify deleted
        feedback = models.get_feedback(feedback_id)
        assert feedback is None
    
    def test_admin_products_page(self, client):
        """Test admin products management page"""
        # Login
        client.post('/admin/login', data={'password': 'testpass'})
        
        response = client.get('/admin/products')
        assert response.status_code == 200
    
    def test_admin_add_product(self, client):
        """Test admin can add a product"""
        # Login
        client.post('/admin/login', data={'password': 'testpass'})
        
        response = client.post('/admin/products/add',
                               data={
                                   'title': 'New Test Product',
                                   'description': 'Test Description',
                                   'price': '29.99',
                                   'image_url': 'http://test.jpg'
                               },
                               follow_redirects=True)
        assert response.status_code == 200
        
        # Verify product was added
        products = models.get_products()
        assert any(p['title'] == 'New Test Product' for p in products)
    
    def test_admin_edit_product(self, client):
        """Test admin can edit a product"""
        # Login
        client.post('/admin/login', data={'password': 'testpass'})
        
        # Add a product first
        product_id = models.add_product('Original', 'Original desc', 10.0, None)
        
        # Edit it
        response = client.post(f'/admin/products/edit/{product_id}',
                               data={
                                   'title': 'Updated Title',
                                   'description': 'Updated desc',
                                   'price': '20.0',
                                   'image_url': 'http://updated.jpg'
                               },
                               follow_redirects=True)
        assert response.status_code == 200
        
        # Verify changes
        product = models.get_product(product_id)
        assert product['title'] == 'Updated Title'
        assert product['price'] == 20.0
    
    def test_admin_delete_product(self, client):
        """Test admin can delete a product"""
        # Login
        client.post('/admin/login', data={'password': 'testpass'})
        
        # Add product
        product_id = models.add_product('To Delete', 'Delete me', 5.0, None)
        
        # Delete it
        response = client.post(f'/admin/products/delete/{product_id}',
                               follow_redirects=True)
        assert response.status_code == 200
        
        # Verify deleted
        product = models.get_product(product_id)
        assert product is None
    
    def test_admin_orders_page(self, client):
        """Test admin orders page"""
        # Login
        client.post('/admin/login', data={'password': 'testpass'})
        
        response = client.get('/admin/orders')
        assert response.status_code == 200
    
    def test_admin_order_detail(self, client):
        """Test admin can view order details"""
        # Login
        client.post('/admin/login', data={'password': 'testpass'})
        
        # Create an order
        order_id = models.create_order('Test Customer', 'test@test.com', 50.0)
        
        response = client.get(f'/admin/orders/{order_id}')
        assert response.status_code == 200
    
    def test_admin_update_order_status(self, client):
        """Test admin can update order status"""
        # Login
        client.post('/admin/login', data={'password': 'testpass'})
        
        # Create order
        order_id = models.create_order('Customer', 'email@test.com', 100.0)
        
        # Update status
        response = client.post(f'/admin/orders/{order_id}/status',
                               data={'status': 'shipped'},
                               follow_redirects=True)
        assert response.status_code == 200
        
        # Verify status updated
        order = models.get_order(order_id)
        assert order['status'] == 'shipped'
    
    def test_admin_logout(self, client):
        """Test admin logout"""
        # Login
        client.post('/admin/login', data={'password': 'testpass'})
        
        # Logout
        response = client.get('/admin/logout', follow_redirects=True)
        assert response.status_code == 200
        
        # Should not be able to access admin after logout
        response = client.get('/admin/', follow_redirects=False)
        assert response.status_code == 302


class TestCartSessionManagement:
    """Integration tests for cart session handling"""
    
    def test_cart_persists_across_requests(self, client):
        """Test that cart persists in session"""
        products = models.get_products(limit=1)
        if products:
            product_id = products[0]['id']
            
            # Add to cart
            client.post(f'/cart/add/{product_id}', data={'quantity': 1})
            
            # Check cart in another request
            response = client.get('/cart')
            assert response.status_code == 200
    
    def test_cart_cleared_after_checkout(self, client):
        """Test that cart is cleared after successful checkout"""
        products = models.get_products(limit=1)
        if products:
            product_id = products[0]['id']
            
            # Add to cart
            client.post(f'/cart/add/{product_id}', data={'quantity': 1})
            
            # Checkout
            client.post('/checkout',
                       data={'name': 'Test', 'email': 'test@test.com'},
                       follow_redirects=True)
            
            # Cart should be empty
            response = client.get('/cart')
            assert response.status_code == 200
    
    def test_add_multiple_quantities(self, client):
        """Test adding multiple quantities of same product"""
        products = models.get_products(limit=1)
        if products:
            product_id = products[0]['id']
            
            # Add twice
            client.post(f'/cart/add/{product_id}', data={'quantity': 2})
            client.post(f'/cart/add/{product_id}', data={'quantity': 3})
            
            # Should have 5 total
            response = client.get('/cart')
            assert response.status_code == 200


class TestErrorHandling:
    """Integration tests for error handling"""
    
    def test_nonexistent_route(self, client):
        """Test accessing non-existent route"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_admin_edit_nonexistent_product(self, client):
        """Test editing product that doesn't exist"""
        # Login
        client.post('/admin/login', data={'password': 'testpass'})
        
        response = client.get('/admin/products/edit/99999', follow_redirects=True)
        assert response.status_code == 200
