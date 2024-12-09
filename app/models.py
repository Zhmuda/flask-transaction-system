from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)
    commission_rate = db.Column(db.Float, default=0.01)
    webhook_url = db.Column(db.String(250), nullable=True)
    role = db.Column(db.String(10), default='user')  # Возможные роли: admin, user

    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, canceled, expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
