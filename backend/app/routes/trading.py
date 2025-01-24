from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import TradingAccount, TradingPosition
from app.services.market_data import get_stock_price, get_forex_rate, get_crypto_price

trading_bp = Blueprint('trading', __name__)

@trading_bp.route('/accounts', methods=['GET'])
@login_required
def get_trading_accounts():
    accounts = TradingAccount.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': account.id,
        'account_type': account.account_type,
        'balance': account.balance
    } for account in accounts]), 200

@trading_bp.route('/positions', methods=['GET'])
@login_required
def get_trading_positions():
    positions = TradingPosition.query.join(TradingAccount).filter(TradingAccount.user_id == current_user.id).all()
    return jsonify([{
        'symbol': pos.symbol,
        'quantity': pos.quantity,
        'entry_price': pos.entry_price,
        'current_price': pos.current_price
    } for pos in positions]), 200

@trading_bp.route('/trade', methods=['POST'])
@login_required
def execute_trade():
    data = request.get_json()
    
    # Validate input
    required_fields = ['symbol', 'quantity', 'trade_type', 'account_type']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required trade parameters'}), 400

    symbol = data['symbol']
    quantity = data['quantity']
    trade_type = data['trade_type']  # 'buy' or 'sell'
    account_type = data['account_type']  # 'stock', 'forex', 'crypto'

    # Get current market price
    try:
        if account_type == 'stock':
            current_price = get_stock_price(symbol)
        elif account_type == 'forex':
            current_price = get_forex_rate(symbol)
        elif account_type == 'crypto':
            current_price = get_crypto_price(symbol)
        else:
            return jsonify({'error': 'Invalid account type'}), 400
    except Exception as e:
        return jsonify({'error': f'Price retrieval failed: {str(e)}'}), 500

    # Find or create trading account
    trading_account = TradingAccount.query.filter_by(
        user_id=current_user.id, 
        account_type=account_type
    ).first()

    if not trading_account:
        trading_account = TradingAccount(
            user_id=current_user.id, 
            account_type=account_type,
            balance=0
        )
        db.session.add(trading_account)

    # Execute trade logic
    total_cost = current_price * quantity
    
    if trade_type == 'buy':
        if trading_account.balance < total_cost:
            return jsonify({'error': 'Insufficient funds'}), 400
        
        trading_account.balance -= total_cost
        
        # Create or update trading position
        position = TradingPosition.query.filter_by(
            trading_account_id=trading_account.id, 
            symbol=symbol
        ).first()

        if position:
            # Update existing position
            position.quantity += quantity
            position.current_price = current_price
        else:
            # Create new position
            position = TradingPosition(
                trading_account_id=trading_account.id,
                symbol=symbol,
                quantity=quantity,
                entry_price=current_price,
                current_price=current_price
            )
            db.session.add(position)

    elif trade_type == 'sell':
        position = TradingPosition.query.filter_by(
            trading_account_id=trading_account.id, 
            symbol=symbol
        ).first()

        if not position or position.quantity < quantity:
            return jsonify({'error': 'Insufficient position'}), 400

        position.quantity -= quantity
        trading_account.balance += total_cost

        if position.quantity == 0:
            db.session.delete(position)

    db.session.commit()

    return jsonify({
        'message': 'Trade executed successfully',
        'account_balance': trading_account.balance
    }), 200
