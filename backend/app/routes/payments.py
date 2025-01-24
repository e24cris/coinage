from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models.user import ManualPaymentRequest, PaymentStatus, User
from datetime import datetime
import os
import uuid

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/request', methods=['POST'])
@login_required
def create_payment_request():
    """
    Create a new manual payment request
    """
    data = request.get_json()
    
    # Validate input
    required_fields = ['amount', 'cryptocurrency', 'wallet_address']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required payment request fields'}), 400

    # Handle payment proof upload if exists
    proof_filename = None
    if 'proof_of_payment' in request.files:
        proof = request.files['proof_of_payment']
        if proof:
            # Generate unique filename
            filename = f"{uuid.uuid4()}_{proof.filename}"
            proof_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'payment_proofs', filename)
            proof.save(proof_path)
            proof_filename = filename

    # Create payment request
    payment_request = ManualPaymentRequest(
        user_id=current_user.id,
        amount=data['amount'],
        cryptocurrency=data['cryptocurrency'],
        wallet_address=data['wallet_address'],
        proof_of_payment=proof_filename,
        status=PaymentStatus.PENDING
    )

    db.session.add(payment_request)
    db.session.commit()

    return jsonify({
        'message': 'Payment request submitted successfully',
        'request': payment_request.to_dict()
    }), 201

@payments_bp.route('/requests', methods=['GET'])
@login_required
def get_user_payment_requests():
    """
    Retrieve user's payment requests
    """
    requests = ManualPaymentRequest.query.filter_by(user_id=current_user.id).all()
    return jsonify([request.to_dict() for request in requests]), 200

@payments_bp.route('/admin/requests', methods=['GET'])
@login_required
def get_all_payment_requests():
    """
    Retrieve all payment requests (admin only)
    """
    # Add admin check
    if not current_user.is_admin:  # Assume you'll add is_admin to User model
        return jsonify({'error': 'Unauthorized access'}), 403

    requests = ManualPaymentRequest.query.filter_by(status=PaymentStatus.PENDING).all()
    return jsonify([request.to_dict() for request in requests]), 200

@payments_bp.route('/admin/process/<int:request_id>', methods=['POST'])
@login_required
def process_payment_request(request_id):
    """
    Process a payment request by admin
    """
    # Add admin check
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.get_json()
    payment_request = ManualPaymentRequest.query.get_or_404(request_id)

    # Validate action
    action = data.get('action')
    if action not in ['approve', 'reject']:
        return jsonify({'error': 'Invalid action'}), 400

    # Process request
    if action == 'approve':
        payment_request.status = PaymentStatus.APPROVED
        payment_request.transaction_hash = data.get('transaction_hash')
        
        # Update user's account balance
        user = User.query.get(payment_request.user_id)
        user.account_balance += payment_request.amount

    else:  # Reject
        payment_request.status = PaymentStatus.REJECTED

    payment_request.processed_at = datetime.utcnow()
    payment_request.admin_notes = data.get('notes', '')

    db.session.commit()

    return jsonify({
        'message': f'Payment request {action}d successfully',
        'request': payment_request.to_dict()
    }), 200
