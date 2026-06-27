import os
from flask import Flask
from dotenv import load_dotenv
from .models import db

# Carrega as variáveis do arquivo .env (apenas para desenvolvimento local)
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # REMOVA O BLOCO COM O db.create_all() POR ENQUANTO
    # Ou apenas comente ele totalmente

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app