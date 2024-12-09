from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

def setup_admin(app):
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
    from app.models import db, User, Transaction
    admin.add_view(SecureModelView(User, db.session))
    admin.add_view(SecureModelView(Transaction, db.session))
