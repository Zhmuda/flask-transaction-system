from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flasgger import Swagger

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    csrf.init_app(app)
    Swagger(app)

    with app.app_context():
        from .routes import bp as main_routes
        from .api.views import bp as api_routes
        from .admin.views import admin_bp

        app.register_blueprint(main_routes)
        app.register_blueprint(api_routes, url_prefix='/api')
        app.register_blueprint(admin_bp, url_prefix='/admin')

        db.create_all()

    return app
