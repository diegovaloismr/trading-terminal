import time
import os
from datetime import datetime, timedelta
from flask import Flask
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


# 🔁 LOOP PRINCIPAL (SEM THREAD)
def loop_principal():
    while True:
        try:
            if dentro_do_horario():
                print("📊 Mercado aberto → executando...")
                main()
            else:
                print("⏸️ Fora do horário (sistema ativo)")

            time.sleep(300)  # 5 minutos

        except Exception as e:
            print("Erro no loop:", e)
            time.sleep(60)


# 🔥 inicia loop em background (mas direto)
import threading
threading.Thread(target=loop_principal, daemon=True).start()

print("🚀 Sistema rodando na nuvem...")

# 🔧 porta dinâmica Railway
port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)
