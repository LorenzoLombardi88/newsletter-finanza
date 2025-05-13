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
    print("Articoli rilevanti della settimana:")
    for article in articles:
        print(f"- {article.get_text()}")

# Funzione per ottenere i tassi di cambio
def get_exchange_rate():
    cr = CurrencyRates()
    rate = cr.get_rate('EUR', 'USD')  # Tasso EUR/USD
    print(f"\nTasso di cambio EUR/USD: {rate}")

# Funzione per ottenere la chiusura degli indici di borsa
def get_stock_market_closures():
    indices = ['^IXIC', '^DJI', '^GSPC']  # NASDAQ, Dow Jones, S&P 500
    print("\nChiusure principali borse mondiali:")
    for index in indices:
        data = yf.download(index, period='1d', interval='1m')
        closing_price = data['Close'][-1]  # Ultima chiusura
        print(f"{index}: {closing_price}")

# Funzione per ottenere le notizie finanziarie (NewsAPI)
def get_news():
    api_key = 'Y9ad037d7a2e54a1d8c5ee5464b4d9782'  # Registrati su NewsAPI per ottenere una chiave API gratuita
    newsapi = NewsApiClient(api_key=api_key)
    articles = newsapi.get_everything(q='finanza', language='it', page_size=5)
    print("\nNotizie finanziarie:")
    for article in articles['articles']:
        print(f"- {article['title']}")

# Funzione principale che raccoglie tutti i dati
def create_newsletter():
    get_articles()
    get_exchange_rate()
    get_stock_market_closures()
    get_news()

# Esegui la funzione
create_newsletter()
