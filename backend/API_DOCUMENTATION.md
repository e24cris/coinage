# Coinage Trading Platform API Documentation

## Overview
This document provides a comprehensive guide to the Coinage Trading Platform's RESTful API endpoints.

## Authentication Routes
### User Registration
- **Endpoint**: `/auth/register`
- **Method**: `POST`
- **Description**: Register a new user account
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: 
    ```json
    {
      "message": "Registration successful",
      "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "account_balance": "float",
        "is_admin": "boolean",
        "registration_date": "datetime"
      }
    }
    ```
- **Error Responses**:
  - 400: Missing required fields
  - 400: Username or email already exists

### User Login
- **Endpoint**: `/auth/login`
- **Method**: `POST`
- **Description**: Authenticate user and create session
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "message": "Login successful",
      "user": {
        "id": "integer",
        "username": "string",
        "email": "string",
        "account_balance": "float",
        "is_admin": "boolean"
      }
    }
    ```
- **Error Responses**:
  - 400: Missing required fields
  - 401: Invalid credentials

### User Logout
- **Endpoint**: `/auth/logout`
- **Method**: `POST`
- **Description**: Terminate user session
- **Authentication**: Required
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "message": "Logged out successfully"
    }
    ```

### Get User Profile
- **Endpoint**: `/auth/profile`
- **Method**: `GET`
- **Description**: Retrieve current user's profile information
- **Authentication**: Required
- **Success Response**:
  - **Code**: 200
  - **Content**: User profile details

## Trading Routes
### Get Trading Accounts
- **Endpoint**: `/trading/accounts`
- **Method**: `GET`
- **Description**: Retrieve user's trading accounts
- **Authentication**: Required
- **Success Response**:
  - **Code**: 200
  - **Content**: List of trading accounts

### Get Trading Positions
- **Endpoint**: `/trading/positions`
- **Method**: `GET`
- **Description**: Retrieve user's current trading positions
- **Authentication**: Required
- **Success Response**:
  - **Code**: 200
  - **Content**: List of active trading positions

### Execute Trade
- **Endpoint**: `/trading/trade`
- **Method**: `POST`
- **Description**: Execute a buy or sell trade
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "symbol": "string",
    "quantity": "integer",
    "trade_type": "string",  // 'buy' or 'sell'
    "account_type": "string"  // 'stock', 'forex', 'crypto'
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: Trade execution details

## Payment Routes
### Create Payment Request
- **Endpoint**: `/payments/request`
- **Method**: `POST`
- **Description**: Create a manual payment request
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "amount": "float",
    "payment_method": "string"
  }
  ```
- **Success Response**:
  - **Code**: 201
  - **Content**: Payment request details

### Get User Payment Requests
- **Endpoint**: `/payments/requests`
- **Method**: `GET`
- **Description**: Retrieve user's payment requests
- **Authentication**: Required
- **Success Response**:
  - **Code**: 200
  - **Content**: List of payment requests

### Admin: Get All Payment Requests
- **Endpoint**: `/payments/admin/requests`
- **Method**: `GET`
- **Description**: Retrieve all payment requests (admin only)
- **Authentication**: Required (Admin)
- **Success Response**:
  - **Code**: 200
  - **Content**: List of all payment requests

### Admin: Process Payment Request
- **Endpoint**: `/payments/admin/process/<request_id>`
- **Method**: `POST`
- **Description**: Approve or reject a payment request
- **Authentication**: Required (Admin)
- **Request Body**:
  ```json
  {
    "status": "string"  // 'approved' or 'rejected'
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: Updated payment request details

## System Routes
### Health Check
- **Endpoint**: `/health`
- **Method**: `GET`
- **Description**: Check system status
- **Success Response**:
  - **Code**: 200
  - **Content**: System health information

## Error Handling
- All error responses include:
  ```json
  {
    "error": "Error description",
    "status": "error_code"
  }
  ```

## Authentication
- Most routes require authentication via session token
- Unauthenticated requests will receive a 401 Unauthorized response

## Rate Limiting
- API has rate limiting to prevent abuse
- Limits vary by endpoint and user type

## Versioning
- Current API Version: v1.0
- Future versions will be prefixed (e.g., `/v2/...`)

## Best Practices
1. Always use HTTPS
2. Store tokens securely
3. Handle errors gracefully
4. Implement proper logging

## Support
For issues or questions, contact: support@coinage.com
