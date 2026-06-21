from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# No seu models.py, atualize a classe Carteira:
class Carteira(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow) # Nova linha
    from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    # Valor que o usuário define para calcular o saldo real
    preco_mercado_atual = db.Column(db.Float, default=0.0)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def total_investido(self):
        return self.preco_compra * self.quantidade