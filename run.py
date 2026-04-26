import schedule
import time
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
from main import main

app = Flask(__name__)


@app.route("/")
def home():
    return "🚀 Radar rodando..."


def dentro_do_horario():
    agora = datetime.utcnow() - timedelta(hours=3)

    if agora.weekday() <= 4:
        if 7 <= agora.hour < 18:
            return True

    return False


def job():
    if dentro_do_horario():
        print("📊 Mercado aberto → executando...")
        main()
    else:
        print("⏸️ Fora do horário (sistema ativo)")


def scheduler_loop():
    schedule.every(5).minutes.do(job)

    while True:
        try:
            schedule.run_pending()
            time.sleep(30)
        except Exception as e:
            print("Erro no loop:", e)
            time.sleep(60)


# 🔥 roda scheduler em paralelo
thread = Thread(target=scheduler_loop)
thread.start()


print("🚀 Sistema rodando na nuvem...")

# 🔥 inicia servidor web (ISS0 SEGURA O RAILWAY)
app.run(host="0.0.0.0", port=8080)
