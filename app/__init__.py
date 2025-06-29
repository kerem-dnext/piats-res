# Creating app/__init__.py - App factory & setup
from flask import Flask
from app.config import Config
from app.extensions import cors, swagger

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Swagger config
    app.config['SWAGGER'] = {
        'title': 'Resume Parser API',
        'uiversion': 3,
        "specs_route": "/api/docs/"
    }
    
    # Initialize extensions 
    cors.init_app(app)
    swagger.init_app(app)
    
    # Register blueprints
    from app.routes.resume_routes import resume_bp
    app.register_blueprint(resume_bp, url_prefix='/api/v1')
    
    return app
