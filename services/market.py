import yfinance as yf


def get_market_data():
    ativos = {
        "SP500": "^GSPC",
        "DXY": "DX-Y.NYB",
        "IBOV": "^BVSP",
        "USD_BRL": "BRL=X"
    }

    dados = {}

    for nome, ticker in ativos.items():
        try:
            data = yf.download(ticker, period="2d", interval="1h", progress=False)

            if data.empty:
                continue

            preco_atual = data["Close"].iloc[-1]
            preco_abertura = data["Open"].iloc[-1]

            variacao = ((preco_atual - preco_abertura) / preco_abertura) * 100

            dados[nome] = round(variacao, 2)

        except Exception as e:
            print(f"Erro em {ticker}: {e}")
            continue

    return dados


def analisar_correlacoes(dados):
    alertas = []

    if not dados:
        return alertas

    sp = dados.get("SP500", 0)
    ibov = dados.get("IBOV", 0)
    dxy = dados.get("DXY", 0)
    dolar = dados.get("USD_BRL", 0)

    if sp > 0.5 and ibov < 0:
        alertas.append("🧠 S&P subindo forte, IBOV fraco → possível atraso no WIN")

    if dxy > 0.3 and dolar < 0:
        alertas.append("🧠 DXY subindo, mas USD/BRL caindo → possível reversão no WDO")

    if sp > 0.5 and ibov > 0.5:
        alertas.append("🔥 Exterior e Brasil alinhados → tendência mais limpa no WIN")

    return alertas
