from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    env = os.getenv("ENVIRONMENT", "development")

    if env == "testing":
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DB")
        app.config['BASE_URL'] = os.getenv("TEST_BASE_URL")
        app.config['TESTING'] = True
    elif env == "production":
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("PROD_DB")
        app.config['BASE_URL'] = os.getenv("PROD_BASE_URL")
        app.config['TESTING'] = False
    else:  # development
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DEV_DB")
        app.config['BASE_URL'] = os.getenv("DEV_BASE_URL")
        app.config['TESTING'] = False

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api = Api(app)

    from .models import UrlModel
    from .resources import Urls

    api.add_resource(Urls, '/api/urls/', '/api/urls/<string:short_code>')

    @app.route('/')
    def home():
        return ({"status" : "OK", "service" : "Shortly URL Shortener"})
    
    return app