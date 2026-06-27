from flask import Flask
from .models import db  # Importa a instância única definida no models.py

def create_app():
    # 1. Cria a instância do Flask
    app = Flask(__name__)
    
    # 2. Configuração do Banco de Dados
    # SQLite local criado na raiz da aplicação
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto_calc.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 3. Inicializa o banco de dados com o app
    db.init_app(app)
    
    # 4. Registra as rotas dentro do contexto da aplicação
    with app.app_context():
        # Cria as tabelas no arquivo .db automaticamente se não existirem
        db.create_all()
        
        # Importa e registra as rotas (Blueprints)
        from .routes import main_bp
        app.register_blueprint(main_bp)
        
    return app