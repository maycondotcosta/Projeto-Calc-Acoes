import os
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    
    # URL do banco vinda do Render (Environment Variables)
    database_url = os.environ.get('DATABASE_URL')
    
    # Corrige se a URL começar com 'postgres://' para 'postgresql://'
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app