from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instância única do banco de dados
db = SQLAlchemy()

class Carteira(db.Model):
    __tablename__ = 'carteira'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)

class Transacao(db.Model):
    __tablename__ = 'transacao'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_mercado_atual = db.Column(db.Float, default=0.0)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def total_investido(self):
        return self.preco_compra * self.quantidade