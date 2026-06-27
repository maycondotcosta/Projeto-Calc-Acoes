import os
from flask import Flask
from .models import db  # Importa o db único do models.py

def create_app():
    app = Flask(__name__)
    
    # Configuração
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 1. Registra o app no db primeiro
    db.init_app(app)
    
    # 2. Usa o contexto para garantir que o app está pronto antes de importar rotas
    with app.app_context():
        from .routes import main_bp
        app.register_blueprint(main_bp)
        
    return app