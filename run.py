import schedule
import time
from datetime import datetime
from main import main

def dentro_do_horario():
agora = datetime.utcnow() - timedelta(hours=3)

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
        print("⏸️ Fora do horário (mantendo sistema ativo)")


# roda a cada 5 minutos
schedule.every(5).minutes.do(job)

print("🚀 Sistema rodando na nuvem...")

# 🔒 LOOP FORÇADO (ESSENCIAL)
while True:
    try:
        schedule.run_pending()
        time.sleep(30)
    except Exception as e:
        print("Erro no loop:", e)
        time.sleep(60)
