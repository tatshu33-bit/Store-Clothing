# Store Clothing REST API Documentation

## Overview

This REST API provides endpoints for managing products and orders in the Store Clothing application. The API is built with Flask and uses SQLite for data persistence.

## Base URL

```
http://127.0.0.1:5000/api
```

## Setup and Installation

### Prerequisites
- Python 3.7+
- pip

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/tatshu33-bit/Store-Clothing.git
cd Store-Clothing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### Products

#### 1. Get All Products

Retrieves a list of all products.

**Endpoint:** `GET /api/products`

**Response:** `200 OK`
```json
{
    "count": 6,
    "products": [
        {
            "id": 1,
            "title": "Product Name",
            "description": "Product description",
            "price": 19.99,
            "image_url": "https://example.com/image.jpg"
        }
    ]
}
```

---

#### 2. Get Single Product

Retrieves details of a specific product.

**Endpoint:** `GET /api/products/{id}`

**Parameters:**
- `id` (integer, path) - Product ID

**Response:** `200 OK`
```json
{
    "id": 1,
    "title": "Product Name",
    "description": "Product description",
    "price": 19.99,
    "image_url": "https://example.com/image.jpg"
}
```

**Error Response:** `404 Not Found`
```json
{
    "error": "Product not found"
}
```

---

#### 3. Create Product

Creates a new product.

**Endpoint:** `POST /api/products`

**Headers:**
- `Content-Type: application/json`

**Request Body:**
```json
{
    "title": "New Product",
    "description": "Product description",
    "price": 29.99,
    "image_url": "https://example.com/image.jpg"
}
```

**Required Fields:**
- `title` (string)
- `price` (number, must be positive)

**Optional Fields:**
- `description` (string)
- `image_url` (string)

**Response:** `201 Created`
```json
{
    "id": 7,
    "message": "Product created successfully",
    "product": {
        "id": 7,
        "title": "New Product",
        "description": "Product description",
        "price": 29.99,
        "image_url": "https://example.com/image.jpg"
    }
}
```

**Error Response:** `400 Bad Request`
```json
{
    "error": "Missing required fields: title and price"
}
```

---

#### 4. Update Product

Updates an existing product.

**Endpoint:** `PUT /api/products/{id}`

**Parameters:**
- `id` (integer, path) - Product ID

**Headers:**
- `Content-Type: application/json`

**Request Body:**
```json
{
    "title": "Updated Product",
    "price": 35.99
}
```

**Note:** All fields are optional. Only provided fields will be updated.

**Response:** `200 OK`
```json
{
    "message": "Product updated successfully",
    "product": {
        "id": 7,
        "title": "Updated Product",
        "description": "Original description",
        "price": 35.99,
        "image_url": "https://example.com/image.jpg"
    }
}
```

**Error Responses:**
- `404 Not Found` - Product doesn't exist
- `400 Bad Request` - Invalid data format

---

#### 5. Delete Product

Deletes a product.

**Endpoint:** `DELETE /api/products/{id}`

**Parameters:**
- `id` (integer, path) - Product ID

**Response:** `200 OK`
```json
{
    "id": 7,
    "message": "Product deleted successfully"
}
```

**Error Response:** `404 Not Found`
```json
{
    "error": "Product not found"
}
```

---

### Orders

#### 6. Get All Orders

Retrieves a list of all orders.

**Endpoint:** `GET /api/orders`

**Response:** `200 OK`
```json
{
    "count": 2,
    "orders": [
        {
            "id": 1,
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "status": "new",
            "total": 79.97,
            "created_at": "2025-12-17 14:58:56"
        }
    ]
}
```

---

#### 7. Get Single Order

Retrieves details of a specific order including items.

**Endpoint:** `GET /api/orders/{id}`

**Parameters:**
- `id` (integer, path) - Order ID

**Response:** `200 OK`
```json
{
    "id": 1,
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "status": "new",
    "total": 79.97,
    "created_at": "2025-12-17 14:58:56",
    "items": [
        {
            "id": 1,
            "product_id": 1,
            "product_title": "Product Name",
            "quantity": 2,
            "price": 19.99
        }
    ]
}
```

**Error Response:** `404 Not Found`
```json
{
    "error": "Order not found"
}
```

---

#### 8. Create Order

Creates a new order with items.

**Endpoint:** `POST /api/orders`

**Headers:**
- `Content-Type: application/json`

**Request Body:**
```json
{
    "customer_name": "Jane Smith",
    "customer_email": "jane@example.com",
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        },
        {
            "product_id": 3,
            "quantity": 1
        }
    ]
}
```

**Required Fields:**
- `customer_name` (string)
- `items` (array) - Must contain at least one item
  - Each item must have:
    - `product_id` (integer) - Must reference existing product
    - `quantity` (integer) - Must be greater than 0

**Optional Fields:**
- `customer_email` (string)

**Response:** `201 Created`
```json
{
    "id": 2,
    "message": "Order created successfully",
    "order": {
        "id": 2,
        "customer_name": "Jane Smith",
        "customer_email": "jane@example.com",
        "status": "new",
        "total": 149.96
    }
}
```

**Error Responses:**
- `400 Bad Request` - Missing required fields or invalid data
- `404 Not Found` - Referenced product doesn't exist

---

## Error Handling

The API uses standard HTTP status codes and returns errors in JSON format:

### Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Error Response Format

```json
{
    "error": "Error message",
    "message": "Additional details (optional)"
}
```

## Testing with Postman

A Postman collection is provided in the repository: `Store_Clothing_API.postman_collection.json`

### Import Collection:
1. Open Postman
2. Click "Import"
3. Select `Store_Clothing_API.postman_collection.json`
4. Run the collection

The collection includes:
- All 8 API endpoints
- Error handling test cases
- Automated test assertions
- Environment variables for dynamic data

## Testing with cURL

### Example: Get All Products
```bash
curl http://127.0.0.1:5000/api/products
```

### Example: Create Product
```bash
curl -X POST http://127.0.0.1:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Product",
    "description": "Product description",
    "price": 29.99
  }'
```

### Example: Update Product
```bash
curl -X PUT http://127.0.0.1:5000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Product",
    "price": 35.99
  }'
```

### Example: Create Order
```bash
curl -X POST http://127.0.0.1:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "items": [
      {"product_id": 1, "quantity": 2}
    ]
  }'
```

## Database Schema

### Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    image_url TEXT
)
```

### Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    customer_email TEXT,
    status TEXT DEFAULT 'new',
    total REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Order Items Table
```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
```

## Best Practices

1. **Content-Type Header:** Always include `Content-Type: application/json` for POST and PUT requests
2. **Error Handling:** Check status codes and handle errors appropriately
3. **Validation:** Validate data before sending to API
4. **Testing:** Use the provided Postman collection for comprehensive testing

## Future Enhancements

- Authentication and authorization
- Pagination for large result sets
- Advanced filtering and sorting
- Rate limiting
- API versioning
- WebSocket support for real-time updates

## Support

For issues or questions, please open an issue on the GitHub repository.

## License

This project is part of the Store Clothing application.
