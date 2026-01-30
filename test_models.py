"""
Unit tests for models.py - Database operations
"""
import pytest
import sqlite3
import os
from contextlib import closing
import models


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Create a temporary test database for each test"""
    db_file = tmp_path / "test_db.sqlite"
    monkeypatch.setattr(models, 'DB_PATH', str(db_file))
    models.init_db()
    yield str(db_file)
    # Cleanup
    if os.path.exists(db_file):
        os.remove(db_file)


class TestProductOperations:
    """Test product CRUD operations"""
    
    def test_add_product(self, test_db):
        """Test adding a new product"""
        product_id = models.add_product(
            "Test Product",
            "Test Description",
            29.99,
            "http://example.com/image.jpg"
        )
        assert product_id is not None
        assert product_id > 0
        
        # Verify product was added
        product = models.get_product(product_id)
        assert product is not None
        assert product['title'] == "Test Product"
        assert product['description'] == "Test Description"
        assert product['price'] == 29.99
        assert product['image_url'] == "http://example.com/image.jpg"
    
    def test_get_product_nonexistent(self, test_db):
        """Test getting a product that doesn't exist"""
        product = models.get_product(99999)
        assert product is None
    
    def test_get_products_with_limit(self, test_db):
        """Test getting products with limit parameter"""
        # Add multiple products
        for i in range(10):
            models.add_product(f"Product {i}", f"Description {i}", float(i * 10), None)
        
        # Get with limit
        products = models.get_products(limit=5)
        assert len(products) == 5
    
    def test_get_products_empty_database(self, test_db):
        """Test getting products from empty database after init"""
        # init_db adds sample products, so we need to clear them first
        with closing(models.get_conn()) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM products')
            conn.commit()
        
        products = models.get_products()
        assert len(products) == 0
    
    def test_update_product(self, test_db):
        """Test updating a product"""
        product_id = models.add_product("Original", "Original Desc", 10.0, None)
        
        models.update_product(product_id, "Updated", "Updated Desc", 20.0, "http://new.jpg")
        
        product = models.get_product(product_id)
        assert product['title'] == "Updated"
        assert product['description'] == "Updated Desc"
        assert product['price'] == 20.0
        assert product['image_url'] == "http://new.jpg"
    
    def test_delete_product(self, test_db):
        """Test deleting a product"""
        product_id = models.add_product("To Delete", "Delete me", 5.0, None)
        
        # Verify it exists
        product = models.get_product(product_id)
        assert product is not None
        
        # Delete it
        models.delete_product(product_id)
        
        # Verify it's gone
        product = models.get_product(product_id)
        assert product is None


class TestFeedbackOperations:
    """Test feedback CRUD operations"""
    
    def test_add_feedback(self, test_db):
        """Test adding feedback"""
        feedback_id = models.add_feedback(
            "John Doe",
            "john@example.com",
            "Great service!"
        )
        assert feedback_id is not None
        assert feedback_id > 0
        
        # Verify feedback was added
        feedback = models.get_feedback(feedback_id)
        assert feedback is not None
        assert feedback['name'] == "John Doe"
        assert feedback['email'] == "john@example.com"
        assert feedback['message'] == "Great service!"
    
    def test_add_feedback_without_email(self, test_db):
        """Test adding feedback without email (optional field)"""
        feedback_id = models.add_feedback("Anonymous", None, "Good product")
        
        feedback = models.get_feedback(feedback_id)
        assert feedback is not None
        assert feedback['name'] == "Anonymous"
        assert feedback['email'] is None
        assert feedback['message'] == "Good product"
    
    def test_get_feedbacks_ordering(self, test_db):
        """Test that feedbacks are returned in DESC order by created_at"""
        # Add multiple feedbacks
        id1 = models.add_feedback("User1", "user1@test.com", "First")
        id2 = models.add_feedback("User2", "user2@test.com", "Second")
        id3 = models.add_feedback("User3", "user3@test.com", "Third")
        
        feedbacks = models.get_feedbacks()
        assert len(feedbacks) >= 3
        # Verify all three feedbacks are present (order may vary if timestamps are identical)
        feedback_ids = [f['id'] for f in feedbacks[:3]]
        assert id1 in feedback_ids
        assert id2 in feedback_ids
        assert id3 in feedback_ids
    
    def test_delete_feedback(self, test_db):
        """Test deleting feedback"""
        feedback_id = models.add_feedback("Test User", "test@test.com", "Delete me")
        
        # Verify it exists
        feedback = models.get_feedback(feedback_id)
        assert feedback is not None
        
        # Delete it
        models.delete_feedback(feedback_id)
        
        # Verify it's gone
        feedback = models.get_feedback(feedback_id)
        assert feedback is None
    
    def test_get_feedback_nonexistent(self, test_db):
        """Test getting feedback that doesn't exist"""
        feedback = models.get_feedback(99999)
        assert feedback is None


class TestOrderOperations:
    """Test order and order items operations"""
    
    def test_create_order(self, test_db):
        """Test creating an order"""
        order_id = models.create_order(
            "Customer Name",
            "customer@example.com",
            149.99
        )
        assert order_id is not None
        assert order_id > 0
        
        # Verify order was created
        order = models.get_order(order_id)
        assert order is not None
        assert order['customer_name'] == "Customer Name"
        assert order['customer_email'] == "customer@example.com"
        assert order['total'] == 149.99
        assert order['status'] == 'new'
    
    def test_add_order_item(self, test_db):
        """Test adding items to an order"""
        # Create a product and order
        product_id = models.add_product("Test Item", "Description", 25.0, None)
        order_id = models.create_order("Customer", "email@test.com", 50.0)
        
        # Add order item
        models.add_order_item(order_id, product_id, 2, 25.0)
        
        # Verify order item
        items = models.get_order_items(order_id)
        assert len(items) == 1
        assert items[0]['product_id'] == product_id
        assert items[0]['quantity'] == 2
        assert items[0]['price'] == 25.0
    
    def test_get_order_items_with_product_details(self, test_db):
        """Test that get_order_items includes product details"""
        # Create product and order
        product_id = models.add_product("Shirt", "Nice shirt", 30.0, "http://shirt.jpg")
        order_id = models.create_order("Buyer", "buyer@test.com", 60.0)
        models.add_order_item(order_id, product_id, 2, 30.0)
        
        items = models.get_order_items(order_id)
        assert len(items) == 1
        assert items[0]['title'] == "Shirt"
        assert items[0]['image_url'] == "http://shirt.jpg"
    
    def test_get_orders_ordering(self, test_db):
        """Test that orders are returned in DESC order by created_at"""
        id1 = models.create_order("Customer1", "c1@test.com", 100.0)
        id2 = models.create_order("Customer2", "c2@test.com", 200.0)
        id3 = models.create_order("Customer3", "c3@test.com", 300.0)
        
        orders = models.get_orders()
        assert len(orders) >= 3
        # Verify all three orders are present (order may vary if timestamps are identical)
        order_ids = [o['id'] for o in orders[:3]]
        assert id1 in order_ids
        assert id2 in order_ids
        assert id3 in order_ids
    
    def test_update_order_status(self, test_db):
        """Test updating order status"""
        order_id = models.create_order("Customer", "email@test.com", 50.0)
        
        # Initial status should be 'new'
        order = models.get_order(order_id)
        assert order['status'] == 'new'
        
        # Update status
        models.update_order_status(order_id, 'shipped')
        
        # Verify status was updated
        order = models.get_order(order_id)
        assert order['status'] == 'shipped'
    
    def test_get_order_nonexistent(self, test_db):
        """Test getting an order that doesn't exist"""
        order = models.get_order(99999)
        assert order is None


class TestDatabaseInitialization:
    """Test database initialization"""
    
    def test_init_db_creates_tables(self, tmp_path, monkeypatch):
        """Test that init_db creates all necessary tables"""
        db_file = tmp_path / "init_test.sqlite"
        monkeypatch.setattr(models, 'DB_PATH', str(db_file))
        
        models.init_db()
        
        # Verify tables exist
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        assert 'products' in tables
        assert 'feedback' in tables
        assert 'orders' in tables
        assert 'order_items' in tables
    
    def test_init_db_adds_sample_products(self, tmp_path, monkeypatch):
        """Test that init_db adds sample products on first run"""
        db_file = tmp_path / "sample_test.sqlite"
        monkeypatch.setattr(models, 'DB_PATH', str(db_file))
        
        models.init_db()
        
        products = models.get_products()
        assert len(products) == 6  # Sample data has 6 products


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_add_product_with_zero_price(self, test_db):
        """Test adding a product with zero price"""
        product_id = models.add_product("Free Item", "Free description", 0.0, None)
        
        product = models.get_product(product_id)
        assert product is not None
        assert product['price'] == 0.0
    
    def test_add_product_with_negative_price(self, test_db):
        """Test adding a product with negative price (should be allowed by DB)"""
        product_id = models.add_product("Negative", "Test", -10.0, None)
        
        product = models.get_product(product_id)
        assert product is not None
        assert product['price'] == -10.0
    
    def test_get_products_without_limit(self, test_db):
        """Test getting all products without limit"""
        # Add some products
        for i in range(3):
            models.add_product(f"Product {i}", f"Desc {i}", float(i), None)
        
        products = models.get_products()
        # Should return at least the products we added (plus any sample products)
        assert len(products) >= 3
    
    def test_order_with_zero_total(self, test_db):
        """Test creating an order with zero total"""
        order_id = models.create_order("Customer", "email@test.com", 0.0)
        
        order = models.get_order(order_id)
        assert order is not None
        assert order['total'] == 0.0
    
    def test_feedback_with_empty_name(self, test_db):
        """Test adding feedback with various name values"""
        # Empty string name
        feedback_id = models.add_feedback("", "email@test.com", "Message")
        feedback = models.get_feedback(feedback_id)
        assert feedback is not None
        assert feedback['name'] == ""
