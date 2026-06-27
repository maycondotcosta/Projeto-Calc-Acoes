import os
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    
    # URL do banco
    db_url = os.environ.get('DATABASE_URL')
    
    # Se a URL não estiver definida (ou falhar), usamos SQLite para não travar o servidor
    if db_url and db_url.startswith("postgresql"):
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Criar tabelas se for SQLite, para evitar erro de tabela não encontrada
    with app.app_context():
        try:
            db.create_all()
        except:
            pass # Ignora erro de conexão com Postgres e tenta subir assim mesmo
        
        from .routes import main_bp
        app.register_blueprint(main_bp)
    
    return app