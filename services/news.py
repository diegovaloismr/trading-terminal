import logging

logger = logging.getLogger(__name__)


def processar_noticias():
    """
    Aqui você já deve ter sua fonte (API ou RSS)
    Mantive genérico para não quebrar seu sistema.
    """
    try:
        # EXEMPLO (substituir pelo seu fetch real)
        noticias = [
            "Fed signals possible rate hike amid inflation concerns",
            "China stimulus boosts growth expectations",
            "Geopolitical tensions increase in Middle East",
        ]
        return noticias

    except Exception as e:
        logger.error(f"[NEWS] Erro ao buscar notícias: {e}")
        return []


def classificar_noticia(texto):
    texto = texto.lower()

    impacto = 1
    peso_pais = 1
    sentimento = 0
    breaking = False

    # 🌍 País
    if any(p in texto for p in ["fed", "usa", "united states", "treasury"]):
        peso_pais = 3
    elif any(p in texto for p in ["china", "pboe"]):
        peso_pais = 2

    # 🔥 Impacto
    if any(p in texto for p in ["rate hike", "inflation", "crisis", "war", "recession"]):
        impacto = 3
    elif any(p in texto for p in ["growth", "stimulus", "cut rates"]):
        impacto = 2

    # 🧠 Sentimento
    if any(p in texto for p in ["growth", "stimulus", "recovery"]):
        sentimento = 1
    elif any(p in texto for p in ["inflation", "crisis", "war", "hawkish"]):
        sentimento = -1

    # ⚡ Breaking
    if any(p in texto for p in ["breaking", "urgent", "just in"]):
        breaking = True
        impacto += 2

    score = sentimento * impacto * peso_pais

    return {
        "texto": texto,
        "impacto": impacto,
        "peso": peso_pais,
        "sentimento": sentimento,
        "breaking": breaking,
        "score": score
    }


def analisar_noticias(noticias):
    try:
        total_score = 0
        breaking_flag = False

        for n in noticias:
            data = classificar_noticia(n)

            total_score += data["score"]

            if data["breaking"]:
                breaking_flag = True

        # 🧠 normalização simples
        if total_score > 5:
            sentimento = 1
        elif total_score < -5:
            sentimento = -1
        else:
            sentimento = 0

        return {
            "sentimento": sentimento,
            "breaking": breaking_flag,
            "score": total_score
        }

    except Exception as e:
        logger.error(f"[NEWS] Erro análise: {e}")
        return {"sentimento": 0, "breaking": False, "score": 0}
