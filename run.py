import schedule
import time
import os
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
from main import main

app = Flask(__name__)


# 🌐 endpoint para manter Railway ativo
@app.route("/")
def home():
    return "🚀 Radar rodando..."


# 🧠 horário do mercado (Brasil UTC-3)
def dentro_do_horario():
    agora = datetime.utcnow() - timedelta(hours=3)

    # segunda a sexta
    if agora.weekday() <= 4:
        if 7 <= agora.hour < 18:
            return True

    return False


# 🚀 execução principal
def job():
    if dentro_do_horario():
        print("📊 Mercado aberto → executando...")
        main()
    else:
        print("⏸️ Fora do horário (sistema ativo)")


# 🔄 loop do scheduler
def scheduler_loop():
    schedule.every(5).minutes.do(job)

    while True:
        try:
            schedule.run_pending()
            time.sleep(30)
        except Exception as e:
            print("Erro no loop:", e)
            time.sleep(60)


# 🔥 inicia scheduler em paralelo
thread = Thread(target=scheduler_loop)
thread.daemon = True
thread.start()

print("🚀 Sistema rodando na nuvem...")


# 🔧 porta dinâmica do Railway
port = int(os.environ.get("PORT", 8080))

# 🔥 servidor web (mantém container vivo)
app.run(host="0.0.0.0", port=port)
