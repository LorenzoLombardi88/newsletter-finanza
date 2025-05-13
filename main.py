import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from newsapi import NewsApiClient

def get_articles():
    url = "https://www.ilsole24ore.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('a', class_='title')[:5]
    articles_list = [f"- {a.get_text(strip=True)}" for a in articles]
    return articles_list

def get_exchange_rate():
    url = "https://api.exchangerate.host/latest?base=EUR&symbols=USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rate = data['rates']['USD']
        return f"Tasso di cambio EUR/USD: {rate:.4f}"
    else:
        return "Errore nel recupero del tasso di cambio."

def get_stock_market_closures():
    indices = {
        '^IXIC': 'NASDAQ',
        '^DJI': 'Dow Jones',
        '^GSPC': 'S&P 500'
    }
    closures = []
    for symbol, name in indices.items():
        data = yf.download(symbol, period='1d', interval='1d')
        if not data.empty:
            close = data['Close'].iloc[-1]
            closures.append(f"{name}: {close:.2f} USD")
    return closures

def get_news():
    api_key = '9ad037d7a2e54a1d8c5ee5464b4d9782'
    newsapi = NewsApiClient(api_key=api_key)
    articles = newsapi.get_everything(q='finanza', language='it', page_size=5)
    return [f"- {a['title']}" for a in articles['articles']]

def send_email(content):
    sender = "lombardilorenzo8824@gmail.com"
    receiver = "lorenzo.lombardi@coesia.com"
    password = "clmg fhpi njka zmrf"  # Puoi sostituirlo con un secret GitHub

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Newsletter Settimanale - Recap"

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

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        print("Email inviata con successo!")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")
    finally:
        server.quit()

def create_and_send_newsletter():
    articles = get_articles()
    exchange_rate = get_exchange_rate()
    closures = get_stock_market_closures()
    news = get_news()
    content = {
        'articles': "\n".join(articles),
        'exchange_rate': exchange_rate,
        'closures': "\n".join(closures),
        'news': "\n".join(news)
    }
    send_email(content)

create_and_send_newsletter()
