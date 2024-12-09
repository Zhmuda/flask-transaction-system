from celery import Celery
from app.models import db, Transaction
from datetime import datetime, timedelta

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def check_expired_transactions():
    threshold = datetime.utcnow() - timedelta(minutes=15)
    transactions = Transaction.query.filter_by(status='pending').filter(Transaction.created_at < threshold).all()

    for transaction in transactions:
        transaction.status = 'expired'
        db.session.add(transaction)
        # Здесь логика отправки webhook
    db.session.commit()
