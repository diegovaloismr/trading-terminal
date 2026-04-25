import tradingeconomics as te
from datetime import datetime

# COLOQUE SUA CHAVE AQUI
te.login('a47c24e4ccb042d:7aev61j7e4a798j')


def get_macro_events():
    hoje = datetime.now().strftime("%Y-%m-%d")

    try:
        eventos = te.getCalendarData(initDate=hoje, endDate=hoje)
        return eventos
    except Exception as e:
        print("Erro ao buscar dados:", e)
        return []


def filtrar_eventos_relevantes(eventos):
    relevantes = []

    for e in eventos:
        try:
            if e.get("Importance") == 3:  # Alto impacto
                relevantes.append({
                    "time": e.get("Date")[11:16],
                    "title": e.get("Event"),
                    "country": e.get("Country")
                })
        except:
            continue

    return relevantes


def formatar_mensagem(eventos):
    agora = datetime.now().strftime("%H:%M")

    if not eventos:
        return f"📅 EVENTOS DO DIA – {agora}\n\nNenhum evento relevante hoje."

    msg = f"📅 EVENTOS DO DIA – {agora}\n\n"

    for e in eventos:
        msg += f"{e['time']} – {e['title']} ({e['country']})\n"

    msg += "\n⚠️ Eventos de alto impacto — atenção no WIN/WDO"

    return msg

from datetime import datetime, timedelta


def checar_eventos_proximos(eventos, minutos_alerta=15):
    agora = datetime.now()
    alertas = []

    for e in eventos:
        try:
            hora_evento = datetime.strptime(e["time"], "%H:%M")
            hora_evento = hora_evento.replace(
                year=agora.year,
                month=agora.month,
                day=agora.day
            )

            diferenca = (hora_evento - agora).total_seconds() / 60

            if 0 < diferenca <= minutos_alerta:
                alertas.append(e)

        except:
            continue

    return alertas
