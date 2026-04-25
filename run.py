import schedule
import time
from datetime import datetime
from main import main

def dentro_do_horario():
    agora = datetime.now()

    # segunda a sexta
    if agora.weekday() <= 4:
        if 7 <= agora.hour < 18:
            return True

    return False


def job():
    if dentro_do_horario():
        print("📊 Mercado aberto → executando...")
        main()
    else:
        print("⏸️ Fora do horário de mercado")


# 🧠 resumo domingo
def resumo_domingo():
    agora = datetime.now()

    if agora.weekday() == 6 and agora.hour == 18:
        print("📅 Gerando resumo semanal...")

        from services.news import processar_noticias

        noticias = processar_noticias()

        for n in noticias[:5]:
            from main import send_message
            send_message(f"📊 RESUMO SEMANAL\n\n{n}")


# ⏱️ agenda
schedule.every(5).minutes.do(job)
schedule.every().hour.do(resumo_domingo)

print("🚀 Sistema rodando na nuvem...")

while True:
    schedule.run_pending()
    time.sleep(30)
