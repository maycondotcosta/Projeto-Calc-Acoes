import os
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    
    # URL do banco
    db_url = os.environ.get('DATABASE_URL')
    
    # Se a conexão falhar no início, o Flask ainda vai subir
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///local.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Define um timeout curto para não travar o site esperando o banco
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'connect_args': {'connect_timeout': 5}}
    
    db.init_app(app)
    
    with app.app_context():
        # Tentamos criar as tabelas apenas se possível
        try:
            db.create_all()
        except:
            print("Aviso: Não foi possível conectar ao banco remoto, rodando em modo limitado.")
        
        from .routes import main_bp
        app.register_blueprint(main_bp)
        
    return app