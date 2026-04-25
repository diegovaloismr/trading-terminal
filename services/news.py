import requests
import time

API_KEY = "cc9552f9b0b440ce99d92fd19491ffc4"

# 🧠 cache de notícias já enviadas
noticias_enviadas = set()


def get_market_news():
    url = f"https://newsapi.org/v2/everything?q=finance OR economy OR fed OR inflation OR interest rate&language=en&sortBy=publishedAt&apiKey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])[:10]

        noticias = []

        for a in articles:
            titulo = a["title"]
            noticias.append(titulo)

        return noticias

    except Exception as e:
        print("Erro ao buscar notícias:", e)
        return []


# 🔍 filtro de relevância
def filtrar_noticias_relevantes(noticias):
    palavras_chave = [
        "inflation", "interest rate", "fed",
        "central bank", "recession", "gdp",
        "oil", "war", "china", "unemployment"
    ]

    relevantes = []

    for n in noticias:
        for palavra in palavras_chave:
            if palavra.lower() in n.lower():
                relevantes.append(n)
                break

    return relevantes


# 🧠 classificar impacto
def classificar_impacto(noticia):
    alto = ["fed", "interest rate", "inflation", "cpi", "central bank"]
    medio = ["gdp", "unemployment", "china", "oil"]

    texto = noticia.lower()

    for p in alto:
        if p in texto:
            return "🔴 ALTO IMPACTO"

    for p in medio:
        if p in texto:
            return "🟡 MÉDIO IMPACTO"

    return "🟢 BAIXO IMPACTO"


# 🧠 traduzir para impacto no mercado
def traduzir_para_mercado(noticia):
    texto = noticia.lower()

    impactos = []

    if "inflation" in texto or "cpi" in texto:
        impactos.append("→ inflação alta pode pressionar juros")
        impactos.append("→ dólar tende a subir (WDO ↑)")
        impactos.append("→ índice pode cair (WIN ↓)")

    if "interest rate" in texto or "fed" in texto:
        impactos.append("→ juros impactam diretamente o fluxo global")
        impactos.append("→ alta de juros favorece dólar (WDO ↑)")
        impactos.append("→ pressão no índice (WIN ↓)")

    if "oil" in texto:
        impactos.append("→ impacto em commodities (PETR)")
        impactos.append("→ pode influenciar o WIN")

    if "china" in texto:
        impactos.append("→ impacto em commodities e VALE")
        impactos.append("→ reflexo direto no WIN")

    if "war" in texto:
        impactos.append("→ aumento de aversão ao risco")
        impactos.append("→ dólar sobe (WDO ↑)")
        impactos.append("→ índice cai (WIN ↓)")

    return impactos


# 🚫 evitar repetição
def noticia_ja_enviada(noticia):
    if noticia in noticias_enviadas:
        return True

    noticias_enviadas.add(noticia)
    return False


# 🚀 função principal
def processar_noticias():
    noticias = get_market_news()
    relevantes = filtrar_noticias_relevantes(noticias)

    mensagens = []

    for n in relevantes:
        if noticia_ja_enviada(n):
            continue

        impacto = classificar_impacto(n)
        efeitos = traduzir_para_mercado(n)

        mensagem = f"📰 NOTÍCIA\n\n{impacto}\n{n}\n\n"

        if efeitos:
            mensagem += "\n".join(efeitos)

        mensagens.append(mensagem)

    return mensagens
