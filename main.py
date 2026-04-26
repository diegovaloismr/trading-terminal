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
from services.news import processar_noticias


# 🧠 CONFIG LOG
logger = logging.getLogger(__name__)


# 🔑 CONFIG
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# 📤 Enviar mensagem Telegram
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
        logger.error(f"[TELEGRAM] Erro ao enviar mensagem: {e}")


# 🚀 FUNÇÃO PRINCIPAL
def main():
    logger.info("[SYSTEM] Iniciando ciclo do radar")

    try:
        # =========================
        # 📅 EVENTOS MACRO
        # =========================
        logger.info("[MACRO] Buscando eventos")

        eventos = get_macro_events()
        relevantes = filtrar_eventos_relevantes(eventos)
        mensagem_macro = formatar_mensagem(relevantes)

        send_message(mensagem_macro)
        logger.info(f"[MACRO] {len(relevantes)} eventos relevantes enviados")

        # =========================
        # 🌎 DADOS DE MERCADO
        # =========================
        logger.info("[MARKET] Coletando dados")

        sp = get_sp500()
        dxy = get_dxy_proxy()
        usd = get_usd_brl()

        logger.info(f"[MARKET] SP500={sp} | DXY={dxy} | USD/BRL={usd}")

        # =========================
        # 🧠 CENÁRIO
        # =========================
        logger.info("[SCENARIO] Analisando cenário")

        sinais = analisar_cenario(sp, dxy, usd)

        for s in sinais:
            send_message(f"🧠 CENÁRIO\n\n{s}")

        logger.info(f"[SCENARIO] {len(sinais)} sinais enviados")

        # =========================
        # 🔥 SCORE
        # =========================
        logger.info("[SCORE] Calculando score")

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
🔥 SCORE DE MERCADO: {score} ({interpretacao})

{chr(10).join(detalhes)}
"""

        send_message(mensagem_score)

        logger.info(f"[SCORE] Score={score} ({interpretacao})")

        # =========================
        # 🚨 MUDANÇA DE REGIME
        # =========================
        logger.info("[REGIME] Verificando mudança")

        mudanca = detectar_mudanca(score)

        if mudanca:
            send_message(mudanca)
            logger.info("[REGIME] Mudança detectada e enviada")

        # =========================
        # 📰 NOTÍCIAS
        # =========================
        logger.info("[NEWS] Buscando notícias")

        noticias = processar_noticias()

        for n in noticias[:3]:
            send_message(n)

        logger.info(f"[NEWS] {len(noticias[:3])} notícias enviadas")

        logger.info("[SYSTEM] Ciclo finalizado com sucesso\n")

    except Exception as e:
        logger.error(f"[SYSTEM] Erro no ciclo principal: {e}")


# ▶️ Execução local
if __name__ == "__main__":
    main()
