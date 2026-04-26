import time
import threading
import logging
from datetime import datetime, timedelta, timezone
from flask import Flask
from main import main

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def home():
    return "🚀 Radar rodando..."


def dentro_do_horario():
    agora = datetime.now(timezone.utc) - timedelta(hours=3)

    if agora.weekday() <= 4:
        if 7 <= agora.hour < 18:
            return True

    return False


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
            logger.error(f"[ERROR] {e}")
            time.sleep(60)


# 🔥 inicia thread (ESSENCIAL)
thread = threading.Thread(target=loop_principal)
thread.daemon = True
thread.start()

logger.info("🚀 Sistema rodando na nuvem...")
