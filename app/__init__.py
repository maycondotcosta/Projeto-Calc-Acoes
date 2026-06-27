import os
from flask import Flask
from dotenv import load_dotenv
from .models import db

# Carrega as variáveis do arquivo .env (apenas para desenvolvimento local)
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Busca a URL do banco. Se não encontrar, cai no SQLite (fallback)
    # A variável DATABASE_URL deve começar com postgresql://
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # db.create_all()  <-- Comentado para evitar erro de conexão/permissão no deploy inicial
        # Se você precisar que as tabelas sejam criadas, certifique-se de que 
        # o usuário do banco no Supabase tem permissão de DDL (Data Definition Language).
        pass
        
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app