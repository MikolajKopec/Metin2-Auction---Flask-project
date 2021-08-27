from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='metin'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAX_CONTENT_PATH'] = 100000
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "You have to be logged in to acces this page."
    login_manager.login_message_category = "error"
    login_manager.init_app(app)

    

    from .views import views
    from .auth import auth
    from .auctioner import auctioner
    app.register_blueprint(views,ulr_prefix='/')
    app.register_blueprint(auth,ulr_prefix='')
    app.register_blueprint(auctioner,ulr_prefix='/')
    from .models import User,Auction
    create_database(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('websites/' + DB_NAME):
        db.create_all(app=app)
        print('Create database')
