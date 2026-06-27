import os
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    
    # URL do banco
    db_url = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # INICIALIZAÇÃO "PREGUIÇOSA"
    # Comente a linha abaixo para ver se o erro desaparece
    # db.init_app(app)
    
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app