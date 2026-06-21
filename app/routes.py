from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Transacao

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Cria nova transação
        nova = Transacao(
            ticker=request.form['ticker'].upper(),
            preco_compra=float(request.form['preco']),
            quantidade=int(request.form['qtd'])
        )
        db.session.add(nova)
        db.session.commit()
        return redirect(url_for('main.index'))

    transacoes = Transacao.query.all()
    
    dados_processados = []
    total_investido_geral = 0
    total_mercado_geral = 0
    
    for t in transacoes:
        # Se não houver preço de mercado definido, usa o de compra (não tem lucro)
        preco_ref = t.preco_mercado_atual if t.preco_mercado_atual > 0 else t.preco_compra
        
        valor_mercado = preco_ref * t.quantidade
        lucro = (preco_ref - t.preco_compra) * t.quantidade
        lucro_pct = ((preco_ref - t.preco_compra) / t.preco_compra * 100) if t.preco_compra > 0 else 0
        
        total_investido_geral += t.total_investido
        total_mercado_geral += valor_mercado
        
        dados_processados.append({
            'id': t.id,
            'ticker': t.ticker,
            'data_compra': t.data_compra,
            'quantidade': t.quantidade,
            'preco_compra': t.preco_compra,
            'total_investido': t.total_investido,
            'preco_mercado_atual': t.preco_mercado_atual,
            'lucro': lucro,
            'lucro_pct': lucro_pct
        })
        
    return render_template(
        'index.html', 
        transacoes=dados_processados, 
        total_geral=total_investido_geral, 
        valor_atual_total=total_mercado_geral
    )

@main_bp.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    transacao = Transacao.query.get_or_404(id)
    transacao.preco_mercado_atual = float(request.form['novo_preco'])
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/excluir/<int:id>')
def excluir(id):
    transacao = Transacao.query.get_or_404(id)
    db.session.delete(transacao)
    db.session.commit()
    return redirect(url_for('main.index'))