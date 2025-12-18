# Test Plans Documentation

This document outlines all test scenarios implemented for the Store-Clothing web application, including unit tests for the database models and integration tests for the API endpoints.

## Table of Contents
1. [Overview](#overview)
2. [Test Environment Setup](#test-environment-setup)
3. [Unit Tests](#unit-tests)
4. [Integration Tests](#integration-tests)
5. [Test Execution](#test-execution)
6. [Coverage Goals](#coverage-goals)

## Overview

The testing strategy covers critical functionalities of the Store-Clothing application:
- **Backend Logic**: Database operations for products, orders, and feedback
- **API Endpoints**: Shop, cart, checkout, feedback, and admin panel
- **Business Logic**: Cart management, order creation, authentication
- **Edge Cases**: Empty states, invalid inputs, error handling

### Testing Framework
- **Unit Tests**: pytest
- **Integration Tests**: Flask test client
- **Coverage**: pytest-cov
- **CI/CD**: GitHub Actions

## Test Environment Setup

### Prerequisites
```bash
pip install -r requirements.txt
```

### Dependencies
- Flask 3.0.0
- pytest 7.4.3
- pytest-cov 4.1.0

### Test Database
Each test uses an isolated SQLite database created in a temporary directory to ensure test independence and prevent data pollution.

## Unit Tests

Unit tests are located in `test_models.py` and focus on testing individual database operations in the `models.py` module.

### Test Class: TestProductOperations

#### 1. test_add_product
**Functionality**: Adding a new product to the database  
**Scenario**: Create a product with all fields and verify it's stored correctly  
**Test Data**:
- Title: "Test Product"
- Description: "Test Description"
- Price: 29.99
- Image URL: "http://example.com/image.jpg"

**Expected Result**: Product is created with correct attributes and returns a valid ID

#### 2. test_get_product_nonexistent
**Functionality**: Retrieving a non-existent product  
**Scenario**: Attempt to get a product with invalid ID  
**Test Data**: Product ID: 99999  
**Expected Result**: Returns None

#### 3. test_get_products_with_limit
**Functionality**: Limiting product query results  
**Scenario**: Add 10 products and retrieve only 5  
**Test Data**: 10 products with sequential IDs  
**Expected Result**: Only 5 products returned

#### 4. test_get_products_empty_database
**Functionality**: Querying products from empty database  
**Scenario**: Clear all products and query  
**Expected Result**: Empty list returned

#### 5. test_update_product
**Functionality**: Updating existing product  
**Scenario**: Create product, then update all fields  
**Test Data**:
- Original: "Original", "Original Desc", 10.0
- Updated: "Updated", "Updated Desc", 20.0, "http://new.jpg"

**Expected Result**: Product fields are updated correctly

#### 6. test_delete_product
**Functionality**: Deleting a product  
**Scenario**: Create product, delete it, verify deletion  
**Expected Result**: Product no longer exists after deletion

### Test Class: TestFeedbackOperations

#### 7. test_add_feedback
**Functionality**: Adding customer feedback  
**Scenario**: Submit feedback with all fields  
**Test Data**:
- Name: "John Doe"
- Email: "john@example.com"
- Message: "Great service!"

**Expected Result**: Feedback saved with correct attributes

#### 8. test_add_feedback_without_email
**Functionality**: Adding feedback without email (optional field)  
**Scenario**: Submit feedback with null email  
**Test Data**: Name: "Anonymous", Email: None, Message: "Good product"  
**Expected Result**: Feedback saved with null email field

#### 9. test_get_feedbacks_ordering
**Functionality**: Feedback retrieval ordering  
**Scenario**: Add 3 feedbacks and verify DESC order by created_at  
**Expected Result**: Most recent feedback appears first

#### 10. test_delete_feedback
**Functionality**: Deleting feedback  
**Scenario**: Create feedback, delete it, verify deletion  
**Expected Result**: Feedback no longer exists

#### 11. test_get_feedback_nonexistent
**Functionality**: Retrieving non-existent feedback  
**Scenario**: Query with invalid ID  
**Expected Result**: Returns None

### Test Class: TestOrderOperations

#### 12. test_create_order
**Functionality**: Creating a customer order  
**Scenario**: Create order with customer details  
**Test Data**:
- Customer: "Customer Name"
- Email: "customer@example.com"
- Total: 149.99

**Expected Result**: Order created with status 'new'

#### 13. test_add_order_item
**Functionality**: Adding items to an order  
**Scenario**: Create product and order, add item  
**Test Data**: Product (25.0), Quantity: 2  
**Expected Result**: Order item created with correct product and quantity

#### 14. test_get_order_items_with_product_details
**Functionality**: Order items include product details  
**Scenario**: Add order item and verify joined product data  
**Expected Result**: Order item includes product title and image

#### 15. test_get_orders_ordering
**Functionality**: Order retrieval ordering  
**Scenario**: Create 3 orders and verify DESC order  
**Expected Result**: Most recent order appears first

#### 16. test_update_order_status
**Functionality**: Updating order status  
**Scenario**: Create order, update status from 'new' to 'shipped'  
**Expected Result**: Status updated correctly

#### 17. test_get_order_nonexistent
**Functionality**: Retrieving non-existent order  
**Scenario**: Query with invalid order ID  
**Expected Result**: Returns None

### Test Class: TestDatabaseInitialization

#### 18. test_init_db_creates_tables
**Functionality**: Database initialization  
**Scenario**: Initialize new database and verify table creation  
**Expected Result**: All required tables exist (products, feedback, orders, order_items)

#### 19. test_init_db_adds_sample_products
**Functionality**: Sample data insertion  
**Scenario**: Initialize database and check for sample products  
**Expected Result**: 6 sample products are created

### Test Class: TestEdgeCases

#### 20. test_add_product_with_zero_price
**Functionality**: Product with zero price  
**Scenario**: Add product with price 0.0  
**Expected Result**: Product created successfully

#### 21. test_add_product_with_negative_price
**Functionality**: Product with negative price  
**Scenario**: Add product with negative price  
**Expected Result**: Product created (validation not enforced at DB level)

#### 22. test_get_products_without_limit
**Functionality**: Query all products  
**Scenario**: Retrieve all products without limit  
**Expected Result**: All products returned

#### 23. test_order_with_zero_total
**Functionality**: Order with zero total  
**Scenario**: Create order with 0.0 total  
**Expected Result**: Order created successfully

#### 24. test_feedback_with_empty_name
**Functionality**: Feedback with empty name  
**Scenario**: Submit feedback with empty string name  
**Expected Result**: Feedback saved with empty name

## Integration Tests

Integration tests are located in `test_integration.py` and test the complete flow from HTTP requests through routes to database operations.

### Test Class: TestShopEndpoints

#### 25. test_index_page
**Functionality**: Home page rendering  
**Endpoint**: GET /  
**Expected Result**: 200 OK, displays store branding

#### 26. test_shop_page_lists_products
**Functionality**: Product listing page  
**Endpoint**: GET /shop  
**Expected Result**: 200 OK, displays product list

#### 27. test_product_detail_page
**Functionality**: Individual product page  
**Endpoint**: GET /product/{id}  
**Test Data**: Valid product ID  
**Expected Result**: 200 OK, displays product details

#### 28. test_product_not_found
**Functionality**: Non-existent product handling  
**Endpoint**: GET /product/99999  
**Expected Result**: 404 Not Found

#### 29. test_cart_view_empty
**Functionality**: Empty cart display  
**Endpoint**: GET /cart  
**Expected Result**: 200 OK, empty cart view

#### 30. test_add_to_cart
**Functionality**: Adding product to cart  
**Endpoint**: POST /cart/add/{id}  
**Test Data**: quantity: 2  
**Expected Result**: 200 OK, product added to session

#### 31. test_remove_from_cart
**Functionality**: Removing product from cart  
**Endpoint**: POST /cart/remove/{id}  
**Expected Result**: 200 OK, product removed from session

#### 32. test_checkout_empty_cart
**Functionality**: Checkout with empty cart  
**Endpoint**: POST /checkout  
**Expected Result**: Redirect to shop

#### 33. test_checkout_with_items
**Functionality**: Complete checkout process  
**Endpoint**: POST /checkout  
**Test Data**:
- name: "John Doe"
- email: "john@example.com"

**Expected Result**: Order created, cart cleared

#### 34. test_checkout_get_request
**Functionality**: Checkout page display  
**Endpoint**: GET /checkout  
**Expected Result**: 200 OK, shows order summary

### Test Class: TestFeedbackEndpoints

#### 35. test_feedback_page_get
**Functionality**: Feedback page display  
**Endpoint**: GET /feedback  
**Expected Result**: 200 OK

#### 36. test_submit_feedback
**Functionality**: Submitting feedback  
**Endpoint**: POST /feedback  
**Test Data**:
- name: "Test User"
- email: "test@example.com"
- message: "Great service!"

**Expected Result**: Feedback saved to database

#### 37. test_submit_feedback_without_name
**Functionality**: Anonymous feedback  
**Endpoint**: POST /feedback  
**Test Data**: Only email and message  
**Expected Result**: Feedback saved with default name

#### 38. test_submit_empty_feedback
**Functionality**: Empty message validation  
**Endpoint**: POST /feedback  
**Test Data**: Empty message field  
**Expected Result**: Validation error, no save

#### 39. test_feedback_displays_existing
**Functionality**: Display existing feedback  
**Endpoint**: GET /feedback  
**Expected Result**: Shows previously submitted feedback

### Test Class: TestAdminEndpoints

#### 40. test_admin_login_page
**Functionality**: Admin login page  
**Endpoint**: GET /admin/login  
**Expected Result**: 200 OK

#### 41. test_admin_login_success
**Functionality**: Successful admin authentication  
**Endpoint**: POST /admin/login  
**Test Data**: password: "testpass"  
**Expected Result**: Session authenticated, redirect to dashboard

#### 42. test_admin_login_failure
**Functionality**: Failed authentication  
**Endpoint**: POST /admin/login  
**Test Data**: password: "wrongpass"  
**Expected Result**: Authentication failure, stay on login page

#### 43. test_admin_dashboard_requires_auth
**Functionality**: Protected route access  
**Endpoint**: GET /admin/  
**Expected Result**: 302 redirect to login when not authenticated

#### 44. test_admin_dashboard_displays_data
**Functionality**: Dashboard data display  
**Endpoint**: GET /admin/  
**Expected Result**: Shows feedbacks, orders, and products

#### 45. test_admin_delete_feedback
**Functionality**: Deleting feedback via admin  
**Endpoint**: POST /admin/feedback/delete/{id}  
**Expected Result**: Feedback deleted from database

#### 46. test_admin_products_page
**Functionality**: Products management page  
**Endpoint**: GET /admin/products  
**Expected Result**: 200 OK, lists all products

#### 47. test_admin_add_product
**Functionality**: Adding product via admin  
**Endpoint**: POST /admin/products/add  
**Test Data**:
- title: "New Test Product"
- description: "Test Description"
- price: "29.99"
- image_url: "http://test.jpg"

**Expected Result**: Product added to database

#### 48. test_admin_edit_product
**Functionality**: Editing product via admin  
**Endpoint**: POST /admin/products/edit/{id}  
**Test Data**: Updated product fields  
**Expected Result**: Product updated in database

#### 49. test_admin_delete_product
**Functionality**: Deleting product via admin  
**Endpoint**: POST /admin/products/delete/{id}  
**Expected Result**: Product deleted from database

#### 50. test_admin_orders_page
**Functionality**: Orders management page  
**Endpoint**: GET /admin/orders  
**Expected Result**: 200 OK, lists all orders

#### 51. test_admin_order_detail
**Functionality**: Order detail view  
**Endpoint**: GET /admin/orders/{id}  
**Expected Result**: 200 OK, shows order details and items

#### 52. test_admin_update_order_status
**Functionality**: Updating order status  
**Endpoint**: POST /admin/orders/{id}/status  
**Test Data**: status: "shipped"  
**Expected Result**: Order status updated

#### 53. test_admin_logout
**Functionality**: Admin logout  
**Endpoint**: GET /admin/logout  
**Expected Result**: Session cleared, redirect to home

### Test Class: TestCartSessionManagement

#### 54. test_cart_persists_across_requests
**Functionality**: Session persistence  
**Scenario**: Add to cart, verify in subsequent request  
**Expected Result**: Cart data persists in session

#### 55. test_cart_cleared_after_checkout
**Functionality**: Cart cleanup after order  
**Scenario**: Checkout and verify cart is empty  
**Expected Result**: Session cart is cleared

#### 56. test_add_multiple_quantities
**Functionality**: Cumulative cart additions  
**Scenario**: Add same product twice with different quantities  
**Expected Result**: Quantities are summed

### Test Class: TestErrorHandling

#### 57. test_nonexistent_route
**Functionality**: 404 handling  
**Endpoint**: GET /nonexistent  
**Expected Result**: 404 Not Found

#### 58. test_admin_edit_nonexistent_product
**Functionality**: Editing non-existent product  
**Endpoint**: GET /admin/products/edit/99999  
**Expected Result**: Error message, redirect

## Test Execution

### Running All Tests
```bash
pytest
```

### Running Unit Tests Only
```bash
pytest test_models.py
```

### Running Integration Tests Only
```bash
pytest test_integration.py
```

### Running with Coverage Report
```bash
pytest --cov=. --cov-report=html
```

### Running Specific Test Class
```bash
pytest test_models.py::TestProductOperations
```

### Running Specific Test
```bash
pytest test_models.py::TestProductOperations::test_add_product
```

## Coverage Goals

### Target Coverage
- **models.py**: 95%+ (database operations)
- **routes/**: 85%+ (API endpoints)
- **app.py**: 80%+ (application setup)

### Coverage Reports
After running tests with coverage, view the HTML report:
```bash
open htmlcov/index.html
```

## Continuous Integration

The project uses GitHub Actions for automated testing. The workflow is defined in `.github/workflows/tests.yml`.

### Triggers
- Push to main, master, develop branches
- All pull requests
- Push to branches matching `copilot/**`

### Test Matrix
Tests run on multiple Python versions:
- Python 3.9
- Python 3.10
- Python 3.11

### Workflow Steps
1. Checkout code
2. Set up Python environment
3. Install dependencies
4. Run unit tests with coverage
5. Run integration tests with coverage
6. Generate combined coverage report
7. Upload coverage to Codecov (optional)

## Test Data

### Sample Products (from init_db)
1. Футболка Classic - 19.99
2. Сорочка Formal - 39.99
3. Куртка Cozy - 89.99
4. Штани Slim - 49.99
5. Сукня Summer - 59.99
6. Кепка Sport - 14.99

### Test Users
- Admin: password "testpass" (configurable in app.config)
- Customers: Various test emails and names

### Edge Cases Covered
- Zero prices
- Negative prices
- Empty strings
- Null values
- Non-existent IDs
- Empty cart operations
- Failed authentication
- Missing required fields

## Security Considerations

### Test Isolation
- Each test uses a temporary database
- No shared state between tests
- Session management tested independently

### Authentication Testing
- Login success/failure scenarios
- Protected route access
- Session-based authorization
- Logout functionality

## Future Enhancements

Potential areas for additional testing:
1. Performance tests for database queries
2. Load testing for API endpoints
3. Frontend JavaScript testing
4. Database migration testing
5. File upload testing (if implemented)
6. Email notification testing (if implemented)
7. Payment processing tests (if implemented)

## Maintenance

### Adding New Tests
1. Follow existing naming conventions
2. Use appropriate fixtures for database isolation
3. Document test scenarios in this file
4. Update coverage goals if needed

### Updating Tests
When modifying application code:
1. Update affected tests
2. Verify coverage hasn't decreased
3. Add tests for new functionality
4. Update this documentation

---

**Last Updated**: 2025-12-18  
**Test Count**: 58+ tests  
**Framework Version**: pytest 7.4.3
