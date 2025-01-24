# Coinage API Specification

## Overview
This document provides a comprehensive specification for the Coinage Trading Platform API.

## Authentication Endpoints

### User Registration
- **Endpoint**: `/auth/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Responses**:
  - `201`: Registration successful
  - `400`: Validation error
  - `409`: User already exists

### User Login
- **Endpoint**: `/auth/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Responses**:
  - `200`: Login successful, returns JWT token
  - `401`: Invalid credentials

## Trading Endpoints

### Get Trading Accounts
- **Endpoint**: `/trading/accounts`
- **Method**: `GET`
- **Authentication**: Required
- **Responses**:
  - `200`: List of trading accounts
  - `401`: Unauthorized

### Execute Trade
- **Endpoint**: `/trading/trade`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "asset": "string",
    "amount": "number",
    "type": "buy|sell"
  }
  ```
- **Responses**:
  - `201`: Trade executed successfully
  - `400`: Invalid trade parameters
  - `403`: Insufficient funds

## Market Data Endpoints

### Get Market Data
- **Endpoint**: `/market/data/{asset}`
- **Method**: `GET`
- **Parameters**:
  - `asset`: Trading asset symbol
- **Responses**:
  - `200`: Market data for specified asset
  - `404`: Asset not found

## Portfolio Endpoints

### Get Portfolio
- **Endpoint**: `/portfolio`
- **Method**: `GET`
- **Authentication**: Required
- **Responses**:
  - `200`: User's portfolio details
  - `401`: Unauthorized

## Payment Endpoints

### Create Payment Request
- **Endpoint**: `/payments/request`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "amount": "number"
  }
  ```
- **Responses**:
  - `201`: Payment request created
  - `400`: Invalid amount
  - `403`: Payment limit exceeded

## Error Handling

### Standard Error Response
```json
{
  "error": "string",
  "code": "string",
  "details": "optional additional information"
}
```

### Common Error Codes
- `VALIDATION_ERROR`: Input validation failed
- `AUTHENTICATION_ERROR`: Authentication failed
- `INSUFFICIENT_FUNDS`: Not enough balance
- `RATE_LIMIT_EXCEEDED`: Too many requests

## Authentication & Security

### JWT Token
- Tokens are valid for 24 hours
- Include in `Authorization` header: `Bearer {token}`

### Rate Limiting
- Maximum 100 requests per minute per endpoint
- Exceeding limit results in temporary block

## Versioning
- Current API Version: `v1`
- Base URL: `/api/v1/`

## Changelog
- **2025-01-23**: Initial API specification
- Added authentication endpoints
- Added trading and market data endpoints

## Support
For API support, contact: `api-support@coinage.com`
