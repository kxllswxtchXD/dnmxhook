from datetime import datetime

def date():
    return datetime.now().strftime('%H:%M - %d/%m/%Y')