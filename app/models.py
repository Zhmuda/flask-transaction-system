from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)
    commission_rate = db.Column(db.Float, default=0.05)
    webhook_url = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), default='user')

    def __repr__(self):
        return f'<User {self.id}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='transactions')

    def __repr__(self):
        return f'<Transaction {self.id}>'
