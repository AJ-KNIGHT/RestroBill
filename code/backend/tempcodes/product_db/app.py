from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./app.db'
    app.secret_key = 'secret-key'

    db.init_app(app)

    from routes import register_routes

    register_routes(app, db)
    migrate = Migrate(app, db)

    return app