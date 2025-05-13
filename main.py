import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
from forex_python.converter import CurrencyRates
import yfinance as yf
from newsapi import NewsApiClient

# Funzione per ottenere articoli rilevanti
def get_articles():
    url = "https://www.ilsole24ore.com/"  # Modifica con il sito di tua scelta
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('a', class_='title')[:5]  # Trova i primi 5 articoli
    articles_list = []
    for article in articles:
        articles_list.append(f"- {article.get_text()}")
    return articles_list

# Funzione per ottenere i tassi di cambio
def get_exchange_rate():
    cr = CurrencyRates()
    rate = cr.get_rate('EUR', 'USD')  # Tasso EUR/USD
    return f"Tasso di cambio EUR/USD: {rate}"

# Funzione per ottenere la chiusura degli indici di borsa
def get_stock_market_closures():
    indices = ['^IXIC', '^DJI', '^GSPC']  # NASDAQ, Dow Jones, S&P 500
    closures = []
    for index in indices:
        data = yf.download(index, period='1d', interval='1m')
        closing_price = data['Close'][-1]  # Ultima chiusura
        closures.append(f"{index}: {closing_price}")
    return closures

# Funzione per ottenere le notizie finanziarie (NewsAPI)
def get_news():
    api_key = '9ad037d7a2e54a1d8c5ee5464b4d9782'  # Registrati su NewsAPI per ottenere una chiave API gratuita
    newsapi = NewsApiClient(api_key=api_key)
    articles = newsapi.get_everything(q='finanza', language='it', page_size=5)
    news_list = []
    for article in articles['articles']:
        news_list.append(f"- {article['title']}")
    return news_list

# Funzione per inviare l'email
def send_email(content):
    # Dati di accesso per il login su Gmail
    sender_email = "lombardilorenzo8824@gmail.com"  # Il tuo indirizzo email
    receiver_email = "lorenzo.lombardi@coesia.com"  # Destinatario
    password = "clmg fhpi njka zmrf"  # La password per le app (non la password del tuo account)

    # Imposta l'oggetto e il corpo dell'email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Newsletter Settimanale - Recap"

    # Corpo dell'email
    body = f"""
    Ciao Lorenzo,

    Ecco il recap della settimana:

    Articoli rilevanti:
    {content['articles']}

    Tassi di cambio EUR/USD:
    {content['exchange_rate']}

    Chiusure principali borse mondiali:
    {content['closures']}

    Notizie finanziarie:
    {content['news']}

    Saluti,
    La tua Newsletter Automatizzata
    """

    msg.attach(MIMEText(body, 'plain'))

    # Connessione al server Gmail e invio dell'email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Sicurezza
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email inviata con successo!")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")
    finally:
        server.quit()

# Funzione principale per raccogliere i dati e inviare l'email
def create_and_send_newsletter():
    # Raccogli i dati
    articles = get_articles()
    exchange_rate = get_exchange_rate()
    closures = get_stock_market_closures()
    news = get_news()

    # Prepara i dati per l'email
    content = {
        'articles': "\n".join(articles),
        'exchange_rate': exchange_rate,
        'closures': "\n".join(closures),
        'news': "\n".join(news)
    }

    # Invia l'email
    send_email(content)

# Esegui la funzione
create_and_send_newsletter()
