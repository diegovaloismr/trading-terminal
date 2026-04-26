def selecionar_noticia_principal(noticias):
    """
    Retorna a notícia mais relevante do momento
    """
    try:
        melhor = None
        melhor_score = 0

        for n in noticias:
            data = classificar_noticia(n)

            score = abs(data["score"])

            if data["breaking"]:
                score += 5

            if score > melhor_score:
                melhor_score = score
                melhor = data

        return melhor

    except Exception as e:
        logger.error(f"[NEWS] Erro seleção principal: {e}")
        return None
