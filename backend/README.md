# Coinage Backend

## Overview
Backend service for the Coinage investment platform, providing authentication, trading, and market data services.

## Features
- User Authentication
- Trading Account Management
- Market Data Retrieval
- Stock/Forex/Crypto Trading Simulation

## Technology Stack
- Flask
- SQLAlchemy
- Flask-Login
- Bcrypt
- Finnhub API
- Alpha Vantage API
- CoinGecko API

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Steps
1. Clone the repository
2. Create a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies
   ```
   pip install -r requirements.txt
   ```
4. Set environment variables
   ```
   export FLASK_APP=run.py
   export FLASK_ENV=development
   ```
5. Initialize database
   ```
   flask db upgrade
   ```
6. Run the application
   ```
   flask run
   ```

## Environment Variables
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection string
- `FINNHUB_API_KEY`: Finnhub market data API key
- `ALPHA_VANTAGE_API_KEY`: Alpha Vantage forex API key

## Testing
```
python -m pytest tests/
```

## API Endpoints

### Authentication
- `POST /auth/register`: User registration
- `POST /auth/login`: User login
- `POST /auth/logout`: User logout
- `GET /auth/profile`: Get user profile

### Trading
- `GET /trading/accounts`: List trading accounts
- `GET /trading/positions`: List trading positions
- `POST /trading/trade`: Execute a trade

## Contributing
Please read `CONTRIBUTING.md` for details on our code of conduct.

## License
MIT License
