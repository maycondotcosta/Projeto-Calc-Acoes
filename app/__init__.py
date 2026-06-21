import os
from flask import Flask
from dotenv import load_dotenv
from .models import db

# Carrega as variáveis do arquivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Busca a URL do banco nas variáveis de ambiente. 
    # Se não encontrar, usa o SQLite como fallback (útil se você esquecer o .env)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Dica: db.create_all() funciona com Postgres, mas no Supabase 
        # a tabela já deve existir conforme configuramos no painel.
        db.create_all()
        
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app