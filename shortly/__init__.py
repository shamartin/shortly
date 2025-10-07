from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()

def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = testing

    db.init_app(app)
    api = Api(app)

    from .models import UrlModel
    from .resources import Urls

    api.add_resource(Urls, '/api/urls/', '/api/urls/<string:short_code>')

    @app.route('/')
    def home():
        return ({"status" : "OK", "service" : "Shortly URL Shortener"})
    
    return app