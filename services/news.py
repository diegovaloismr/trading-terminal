import logging

logger = logging.getLogger(__name__)


# =========================
# 📰 BUSCAR NOTÍCIAS
# =========================
def processar_noticias():
    try:
        # 🔹 Simulação (depois você conecta API real)
        noticias = [
            "Fed signals possible rate hike amid inflation concerns",
            "China stimulus boosts growth expectations",
            "Geopolitical tensions increase in Middle East",
        ]
        return noticias

    except Exception as e:
        logger.error(f"[NEWS] Erro ao buscar notícias: {e}")
        return []


# =========================
# 🧠 CLASSIFICAÇÃO
# =========================
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


# =========================
# 📊 ANÁLISE GERAL
# =========================
def analisar_noticias(noticias):
    try:
        total_score = 0
        breaking_flag = False

        for n in noticias:
            data = classificar_noticia(n)

            total_score += data["score"]

            if data["breaking"]:
                breaking_flag = True

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


# =========================
# 🏆 NOTÍCIA PRINCIPAL
# =========================
def selecionar_noticia_principal(noticias):
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
