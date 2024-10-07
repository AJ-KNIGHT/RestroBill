from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    # db config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./app.db'
    app.secret_key = 'resturant-app-secret-key'

    db.init_app(app)

    #login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import Users

    @login_manager.user_loader
    def load_user(uid):
        return Users.query.get(uid)

    # custom Unautorized access page
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('auth_error', msg="Only authorized users can access this page. Please log in to continue."))

    bcrypt = Bcrypt(app)

    from routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app
