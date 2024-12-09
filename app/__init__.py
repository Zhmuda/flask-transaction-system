from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_wtf.csrf import CSRFProtect
from app.models import db
from app.admin.views import setup_admin
from app.api.views import api

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Инициализация расширений
    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)

    # Подключение админки
    setup_admin(app)

    # Регистрация Blueprint'ов
    app.register_blueprint(api, url_prefix='/api')

    return app
