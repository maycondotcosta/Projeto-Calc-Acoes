from flask import Blueprint, render_template, request, redirect, url_for
from collections import defaultdict
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
    
    # Dicionário para agrupar dados por Ticker (Consolidação)
    resumo = defaultdict(lambda: {'qtd': 0, 'total_investido': 0, 'preco_atual': 0})
    
    for t in transacoes:
        resumo[t.ticker]['qtd'] += t.quantidade
        resumo[t.ticker]['total_investido'] += (t.preco_compra * t.quantidade)
        # O preço de mercado atualizado sobrescreve o anterior se existir
        if t.preco_mercado_atual > 0:
            resumo[t.ticker]['preco_atual'] = t.preco_mercado_atual
        elif resumo[t.ticker]['preco_atual'] == 0:
            # Caso não tenha preço atual, assume o preço de compra para não ficar zerado
            resumo[t.ticker]['preco_atual'] = t.preco_compra

    # Processamento para o template
    dados_processados = []
    total_investido_geral = 0
    total_mercado_geral = 0
    
    for ticker, info in resumo.items():
        preco_medio = info['total_investido'] / info['qtd'] if info['qtd'] > 0 else 0
        valor_mercado = info['qtd'] * info['preco_atual']
        lucro_financeiro = valor_mercado - info['total_investido']
        
        total_investido_geral += info['total_investido']
        total_mercado_geral += valor_mercado
        
        dados_processados.append({
            'ticker': ticker,
            'quantidade': info['qtd'],
            'preco_medio': preco_medio,
            'valor_mercado': valor_mercado,
            'lucro': lucro_financeiro
        })
        
    return render_template(
        'index.html', 
        transacoes=dados_processados, 
        total_geral=total_investido_geral, 
        valor_atual_total=total_mercado_geral
    )

@main_bp.route('/atualizar/<ticker>', methods=['POST'])
def atualizar(ticker):
    # Atualiza todas as transações daquele ticker com o novo preço de mercado
    novo_preco = float(request.form['novo_preco'])
    transacoes = Transacao.query.filter_by(ticker=ticker).all()
    for t in transacoes:
        t.preco_mercado_atual = novo_preco
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/excluir/<int:id>')
def excluir(id):
    transacao = Transacao.query.get_or_404(id)
    db.session.delete(transacao)
    db.session.commit()
    return redirect(url_for('main.index'))