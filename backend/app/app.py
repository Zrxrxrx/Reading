from flask import Flask
from .extensions import db
from .auth import auth_bp
from .admin import admin_bp
from .book import bookapi
from .user import user_bp
from .collection import collection_bp
from .rate import rate_bp


from .utils.init import init_data

def create_app():
    app = Flask(__name__)

    configure_db(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(bookapi, url_prefix='/book')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(collection_bp, url_prefix='/collection')
    app.register_blueprint(rate_bp, url_prefix='/rate')

    @app.route('/')
    def hello():
        # for test
        return 'Hello World'


    return app

def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        init_data()

