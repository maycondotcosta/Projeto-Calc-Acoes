import os
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    
    # Define o caminho do banco SQLite dentro do projeto
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Cria o arquivo do banco se não existir
        db.create_all()
        
        from .routes import main_bp
        app.register_blueprint(main_bp)
        
    return app