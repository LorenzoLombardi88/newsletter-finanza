import datetime

def generate_newsletter():
    today = datetime.date.today()
    print(f"📰 Newsletter finanziaria - Settimana del {today}")
    print("-" * 50)
    print("Questa è una versione di prova della tua newsletter automatica.")
    print("Contenuti futuri:")
    print("1. Recap della settimana")
    print("2. 5 articoli rilevanti")
    print("3. Tassi di cambio EUR/CCY")
    print("4. Chiusure principali borse mondiali")

if __name__ == "__main__":
    generate_newsletter()
