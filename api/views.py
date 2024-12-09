from flask import Blueprint, request, jsonify
from app.models import db, User, Transaction
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/create_transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    commission = amount * user.commission_rate
    transaction = Transaction(amount=amount, commission=commission, user_id=user.id)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'transaction_id': transaction.id, 'status': transaction.status})

@api.route('/cancel_transaction', methods=['POST'])
def cancel_transaction():
    data = request.get_json()
    transaction_id = data.get('transaction_id')

    transaction = Transaction.query.get(transaction_id)
    if not transaction or transaction.status != 'pending':
        return jsonify({'error': 'Invalid transaction'}), 400

    transaction.status = 'canceled'
    db.session.commit()
    return jsonify({'transaction_id': transaction.id, 'status': transaction.status})

@api.route('/check_transaction/<int:transaction_id>', methods=['GET'])
def check_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    return jsonify({
        'transaction_id': transaction.id,
        'status': transaction.status,
        'amount': transaction.amount,
        'commission': transaction.commission
    })
