import yfinance as yf

def buscar_precos_em_lote(tickers_lista):
    if not tickers_lista:
        return {}
    
    # Prepara a lista com sufixo .SA obrigatório para B3
    tickers_set = set(tickers_lista)
    tickers_formatados = [f"{t}.SA" if not t.endswith('.SA') else t for t in tickers_set]
    tickers_str = " ".join(tickers_formatados)
    
    try:
        # Busca os dados em lote
        data = yf.Tickers(tickers_str).history(period="1d", group_by='ticker')
        
        precos = {}
        for t in tickers_set:
            ticker_busca = f"{t}.SA" if not t.endswith('.SA') else t
            try:
                # Verifica se o ticker existe na resposta
                if ticker_busca in data.columns.levels[0]:
                    preco = data[ticker_busca]['Close'].iloc[-1]
                    precos[t] = float(preco) if preco else 0.0
                else:
                    precos[t] = 0.0
            except:
                precos[t] = 0.0
        return precos
    except:
        return {t: 0.0 for t in tickers_set}