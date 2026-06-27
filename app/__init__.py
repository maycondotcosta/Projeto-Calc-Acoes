import os
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    
    # Tenta usar o Postgres, se falhar ou não existir, usa SQLite
    db_url = os.environ.get('DATABASE_URL')
    
    if db_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
        # Fallback para SQLite caso o Postgres esteja inacessível
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Cria as tabelas no arquivo local se for SQLite
        db.create_all()
        
        from .routes import main_bp
        app.register_blueprint(main_bp)
        
    return app