import logging

logger = logging.getLogger(__name__)


def gerar_entrada(sp, dxy, usd, score, news_data):
    sinais = []

    sentimento = news_data["sentimento"]
    breaking = news_data["breaking"]

    try:
        # ⚡ BLOQUEIO por breaking negativo
        if breaking and sentimento < 0:
            logger.info("[ENTRY] Bloqueado por breaking negativo")
            return []

        # 📈 WIN COMPRA
        if sp > 0 and dxy < 0 and score >= 2 and sentimento >= 0:
            sinais.append({
                "tipo": "WIN",
                "acao": "COMPRA",
                "msg": "Risco ON confirmado + notícias alinhadas"
            })

        # 📉 WIN VENDA
        if sp < 0 and dxy > 0 and score <= -2 and sentimento <= 0:
            sinais.append({
                "tipo": "WIN",
                "acao": "VENDA",
                "msg": "Risco OFF confirmado + notícias negativas"
            })

        # 💵 WDO COMPRA
        if dxy > 0 and usd > 0 and score <= -2:
            sinais.append({
                "tipo": "WDO",
                "acao": "COMPRA",
                "msg": "Dólar forte + cenário macro"
            })

        # 💵 WDO VENDA
        if dxy < 0 and usd < 0 and score >= 2:
            sinais.append({
                "tipo": "WDO",
                "acao": "VENDA",
                "msg": "Dólar fraco + cenário macro"
            })

        return sinais

    except Exception as e:
        logger.error(f"[ENTRY] Erro: {e}")
        return []
