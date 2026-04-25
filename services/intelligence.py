def analisar_cenario(sp500, dxy, usd_brl):
    sinais = []

    if sp500 is None:
        sinais.append("⚠️ S&P indisponível")

    if dxy is None:
        sinais.append("⚠️ DXY indisponível")

    if usd_brl is None:
        sinais.append("⚠️ USD/BRL indisponível")

    if sp500 is None and dxy is None and usd_brl is None:
        return ["⚠️ Sem dados suficientes para análise"]

    if sp500 is not None and dxy is not None:
        if sp500 > 0.3 and dxy < 0:
            sinais.append("📈 RISCO ON → favorece alta no WIN e queda no WDO")

        if sp500 < -0.3 and dxy > 0:
            sinais.append("📉 RISCO OFF → favorece queda no WIN e alta no WDO")

    if usd_brl is not None:
        if usd_brl > 5.2:
            sinais.append("💵 Dólar forte → pressão no índice")

    return sinais


def calcular_score(sp500, dxy, usd_brl):
    score = 0
    detalhes = []

    # 📊 S&P 500 (peso alto)
    if sp500 is not None:
        if sp500 > 1.0:
            score += 2
            detalhes.append("S&P MUITO forte")
        elif sp500 > 0.3:
            score += 1
            detalhes.append("S&P forte")
        elif sp500 < -1.0:
            score -= 2
            detalhes.append("S&P MUITO fraco")
        elif sp500 < -0.3:
            score -= 1
            detalhes.append("S&P fraco")

    # 💵 DXY (peso alto inverso)
    if dxy is not None:
        if dxy > 0.8:
            score -= 2
            detalhes.append("Dólar MUITO forte")
        elif dxy > 0.3:
            score -= 1
            detalhes.append("Dólar forte")
        elif dxy < -0.8:
            score += 2
            detalhes.append("Dólar MUITO fraco")
        elif dxy < -0.3:
            score += 1
            detalhes.append("Dólar fraco")

    # 🇧🇷 U/BRL
    if usd_brl is not None:
        if usd_brl > 5.3:
            score -= 1
            detalhes.append("Real muito fraco")
        elif usd_brl < 4.9:
            score += 1
            detalhes.append("Real forte")

    # 🧠 DETECÇÃO DE CONFLITO
    if sp500 is not None and dxy is not None:
        if sp500 > 0.5 and dxy > 0.5:
            detalhes.append("⚠️ Conflito: bolsa sobe com dólar forte")
        if sp500 < -0.5 and dxy < -0.5:
            detalhes.append("⚠️ Conflito: bolsa cai com dólar fraco")

    return score, detalhes

from services.state import get_last_score, set_last_score


def detectar_mudanca(score):
    ultimo = get_last_score()

    # primeira execução
    if ultimo is None:
        set_last_score(score)
        return None

    diferenca = score - ultimo

    # mudança relevante
    if abs(diferenca) >= 2:
        set_last_score(score)
        return f"🚨 MUDANÇA DE REGIME\n\nScore: {ultimo} → {score}"

    set_last_score(score)
    return None
