import requests
import os
import logging

# 📊 Macro
from services.macro import (
    get_macro_events,
    filtrar_eventos_relevantes,
    formatar_mensagem,
)

# 🌎 Mercado
from services.market_api import (
    get_usd_brl,
    get_sp500,
    get_dxy_proxy,
)

# 🧠 Inteligência
from services.intelligence import (
    analisar_cenario,
    calcular_score,
    detectar_mudanca,
)

# 📰 Notícias
from services.news import (
    processar_noticias,
    analisar_noticias,
    selecionar_noticia_principal,
)

# ⚡ Entrada
from services.entry import gerar_entrada


# =========================
# 🧠 LOG
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


# =========================
# 🔑 CONFIG
# =========================
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# =========================
# 📤 TELEGRAM
# =========================
def send_message(text):
    if not TOKEN or not CHAT_ID:
        logger.warning("[TELEGRAM] TOKEN ou CHAT_ID não configurados")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        requests.post(url, data=payload)
        logger.info("[TELEGRAM] Mensagem enviada")
    except Exception as e:
        logger.error(f"[TELEGRAM] Erro: {e}")


# =========================
# 🚀 MAIN
# =========================
def main():
    logger.info("[SYSTEM] Iniciando ciclo do radar")

    try:

        # =========================
        # 📅 MACRO
        # =========================
        logger.info("[MACRO] Buscando eventos")

        eventos = get_macro_events()
        relevantes = filtrar_eventos_relevantes(eventos)
        mensagem_macro = formatar_mensagem(relevantes)

        send_message(mensagem_macro)
        logger.info(f"[MACRO] {len(relevantes)} eventos enviados")

        # =========================
        # 🌎 MERCADO
        # =========================
        logger.info("[MARKET] Coletando dados")

        sp = get_sp500()
        dxy = get_dxy_proxy()
        usd = get_usd_brl()

        logger.info(f"[MARKET] SP500={sp} | DXY={dxy} | USD={usd}")

        # =========================
        # 🧠 CENÁRIO
        # =========================
        logger.info("[SCENARIO] Analisando")

        sinais = analisar_cenario(sp, dxy, usd)

        for s in sinais:
            send_message(f"🧠 CENÁRIO\n\n{s}")

        logger.info(f"[SCENARIO] {len(sinais)} sinais")

        # =========================
        # 🔥 SCORE
        # =========================
        logger.info("[SCORE] Calculando")

        score, detalhes = calcular_score(sp, dxy, usd)

        interpretacao = "NEUTRO"

        if score >= 3:
            interpretacao = "🚀 FORTE ALTA"
        elif score >= 1:
            interpretacao = "📈 ALTA"
        elif score <= -3:
            interpretacao = "💥 FORTE QUEDA"
        elif score <= -1:
            interpretacao = "📉 QUEDA"

        mensagem_score = f"""
🔥 SCORE: {score} ({interpretacao})

{chr(10).join(detalhes)}
"""

        send_message(mensagem_score)
        logger.info(f"[SCORE] {score} ({interpretacao})")

        # =========================
        # 📰 NEWS
        # =========================
        logger.info("[NEWS] Processando notícias")

        noticias = processar_noticias()
        news_data = analisar_noticias(noticias)
        noticia_principal = selecionar_noticia_principal(noticias)

        logger.info(
            f"[NEWS] Sentimento={news_data['sentimento']} | "
            f"Breaking={news_data['breaking']} | Score={news_data['score']}"
        )

        # 📢 Envia notícia relevante
        if noticia_principal:
            if noticia_principal["impacto"] >= 2 or noticia_principal["breaking"]:

                mensagem_news = f"""
📰 ATUALIZAÇÃO DE MERCADO

{noticia_principal['texto']}

Impacto: {noticia_principal['impacto']}
Sentimento: {noticia_principal['sentimento']}
⚡ Breaking: {noticia_principal['breaking']}
"""
                send_message(mensagem_news)
                logger.info("[NEWS] Notícia enviada")

        # =========================
        # ⚡ ENTRY
        # =========================
        logger.info("[ENTRY] Avaliando entradas")

        entradas = gerar_entrada(sp, dxy, usd, score, news_data)

        if entradas:
            for e in entradas:

                mensagem = f"""
⚡ ENTRADA DETECTADA

Ativo: {e['tipo']}
Ação: {e['acao']}

🧠 Contexto:
{e['msg']}
"""

                if news_data["breaking"] or abs(news_data["score"]) >= 5:
                    mensagem += f"""

📰 Contexto de notícia:
Sentimento: {news_data['sentimento']}
Impacto relevante no mercado
"""

                send_message(mensagem)

            logger.info(f"[ENTRY] {len(entradas)} entradas enviadas")

        else:
            logger.info("[ENTRY] Nenhuma entrada válida")

        # =========================
        # 🚨 REGIME
        # =========================
        logger.info("[REGIME] Verificando")

        mudanca = detectar_mudanca(score)

        if mudanca:
            send_message(mudanca)
            logger.info("[REGIME] Mudança detectada")

        logger.info("[SYSTEM] Ciclo finalizado\n")

    except Exception as e:
        logger.error(f"[SYSTEM] Erro geral: {e}")


if __name__ == "__main__":
    main()
