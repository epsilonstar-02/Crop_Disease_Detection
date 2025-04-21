# app/__init__.py
from flask import Flask
from flask_cors import CORS
from backend.utils.config import API_HOST, API_PORT

def create_app():
    """
    Create and configure the Flask application
    """
    app = Flask(__name__)
    
    CORS(app)
    
    from backend.app.routes import api
    app.register_blueprint(api)
    
    return app 