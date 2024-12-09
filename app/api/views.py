from flask import Blueprint, request, jsonify
from app import db
from app.models import Transaction, User
from datetime import datetime
from flasgger import swag_from

bp = Blueprint('api', __name__)

@bp.route('/create_transaction', methods=['POST'])
@swag_from({
    'tags': ['Transactions'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer'},
                    'amount': {'type': 'number'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Transaction created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'transaction_id': {'type': 'integer'},
                    'status': {'type': 'string'}
                }
            }
        }
    }
})
def create_transaction():
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    commission = amount * user.commission_rate
    transaction = Transaction(user_id=user_id, amount=amount, commission=commission)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'transaction_id': transaction.id, 'status': transaction.status})

@bp.route('/cancel_transaction', methods=['POST'])
@swag_from({
    'tags': ['Transactions'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'transaction_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Transaction canceled successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'transaction_id': {'type': 'integer'},
                    'status': {'type': 'string'}
                }
            }
        }
    }
})
def cancel_transaction():
    data = request.json
    transaction_id = data.get('transaction_id')

    transaction = Transaction.query.get(transaction_id)
    if not transaction or transaction.status != 'pending':
        return jsonify({'error': 'Transaction not found or not cancelable'}), 404

    transaction.status = 'canceled'
    db.session.commit()
    return jsonify({'transaction_id': transaction.id, 'status': transaction.status})

@bp.route('/check_transaction/<int:transaction_id>', methods=['GET'])
@swag_from({
    'tags': ['Transactions'],
    'parameters': [
        {
            'name': 'transaction_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID of the transaction to check'
        }
    ],
    'responses': {
        200: {
            'description': 'Transaction details retrieved',
            'schema': {
                'type': 'object',
                'properties': {
                    'transaction_id': {'type': 'integer'},
                    'status': {'type': 'string'},
                    'amount': {'type': 'number'},
                    'commission': {'type': 'number'}
                }
            }
        }
    }
})
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
