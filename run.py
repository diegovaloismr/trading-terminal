import time
import os
import threading
from datetime import datetime, timedelta, timezone
from flask import Flask
from main import main

app = Flask(__name__)


@app.route("/")
def home():
    return "🚀 Radar rodando..."


# 🧠 horário do mercado (Brasil UTC-3)
def dentro_do_horario():
    agora = datetime.now(timezone.utc) - timedelta(hours=3)

    if agora.weekday() <= 4:
        if 7 <= agora.hour < 18:
            return True

    return False


# 🔁 LOOP PRINCIPAL
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


print("🚀 Sistema rodando na nuvem...")


# 🔥 INICIA LOOP EM THREAD (DIRETO)
thread = threading.Thread(target=loop_principal)
thread.daemon = True
thread.start()


# 🔧 porta Railway
port = int(os.environ.get("PORT", 8080))

# 🔥 servidor web (mantém container vivo)
app.run(host="0.0.0.0", port=port)
