from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/",
    )

    # Set the default database URI to one of your binds
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./active_data.db"

    # Multiple database binds
    app.config["SQLALCHEMY_BINDS"] = {
        'active_data': 'sqlite:///./active_data.db',
        'current_year_data': 'sqlite:///./current_year_data.db',
        'archive_data': 'sqlite:///./archive_data.db'
    }
    app.secret_key = "restrobill-webapp-secret-key"

    db.init_app(app)

    # Make sure to call create_all() to create all tables if they do not exist
    with app.app_context():
        db.create_all()

    # login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import Users, Products, Bill, Sales, ArchivedBill, ArchivedSales

    @login_manager.user_loader
    def load_user(uid):
        return Users.query.get(uid)

    # Custom Unauthorized access page
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(
            url_for(
                "auth_error",
                msg="Only authorized users can access this page. Please log in to continue.",
            )
        )

    bcrypt = Bcrypt(app)

    from routes import register_routes

    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)
    with app.app_context():
        migrate.init_app(app, db)

    return app

