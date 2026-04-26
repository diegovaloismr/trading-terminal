import time
import os
import threading
import logging
from datetime import datetime, timedelta, timezone
from flask import Flask
from main import main

# 🧠 CONFIG LOG
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def home():
    return "🚀 Radar rodando..."


# 🧠 horário do mercado (BRT)
def dentro_do_horario():
    agora = datetime.now(timezone.utc) - timedelta(hours=3)

    if agora.weekday() <= 4:
        if 7 <= agora.hour < 18:
            return True

    return False


# 🔁 LOOP PRINCIPAL
def loop_principal():
    logger.info("Loop principal iniciado")

    while True:
        try:
            if dentro_do_horario():
                logger.info("[MARKET] Mercado aberto → executando")
                main()
            else:
                logger.info("[MARKET] Fora do horário")

            time.sleep(300)

        except Exception as e:
            logger.error(f"[ERROR] Erro no loop: {e}")
            time.sleep(60)


logger.info("🚀 Sistema rodando na nuvem...")

# 🔥 THREAD
thread = threading.Thread(target=loop_principal)
thread.daemon = True
thread.start()

# 🔧 PORTA
port = int(os.environ.get("PORT", 8080))

# 🚀 SERVIDOR
app.run(host="0.0.0.0", port=port)
