import requests
import os

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


# 🔑 CONFIG (Railway usa variáveis de ambiente)
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# 📤 Enviar mensagem para Telegram
def send_message(text):
    if not TOKEN or not CHAT_ID:
        print("⚠️ TOKEN ou CHAT_ID não configurados")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)


# 🚀 FUNÇÃO PRINCIPAL
def main():
    print("🚀 Executando ciclo do radar...")

    # =========================
    # 📅 EVENTOS MACRO
    # =========================
    eventos = get_macro_events()
    relevantes = filtrar_eventos_relevantes(eventos)
    mensagem_macro = formatar_mensagem(relevantes)

    send_message(mensagem_macro)

    # =========================
    # 🌎 DADOS DE MERCADO
    # =========================
    sp = get_sp500()
    dxy = get_dxy_proxy()
    usd = get_usd_brl()

    # =========================
    # 🧠 CENÁRIO
    # =========================
    sinais = analisar_cenario(sp, dxy, usd)

    for s in sinais:
        send_message(f"🧠 CENÁRIO\n\n{s}")

    # =========================
    # 🔥 SCORE DE MERCADO
    # =========================
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

    # =========================
    # 🚨 MUDANÇA DE REGIME
    # =========================
    mudanca = detectar_mudanca(score)

    if mudanca:
        send_message(mudanca)

    # =========================
    # 📰 NOTÍCIAS
    # =========================
    noticias = processar_noticias()

    for n in noticias[:3]:
        send_message(n)

    print("✅ Ciclo finalizado\n")


# ▶️ Execução local (opcional)
if __name__ == "__main__":
    main()
