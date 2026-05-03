import os
import time
import requests
import yfinance as yf

# 🔑 TELEGRAM AYARLARI (Railway Variables'tan gelir)
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 📱 TELEGRAM MESAJ GÖNDERME
def send(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        print("Telegram gönderilemedi")

# 📊 HİSSE LİSTESİ (basit BIST 100 çekirdek)
stocks = [
    "THYAO.IS","EREGL.IS","SISE.IS","AKBNK.IS","KCHOL.IS",
    "YKBNK.IS","GARAN.IS","ASELS.IS","TUPRS.IS","BIMAS.IS",
    "SAHOL.IS","FROTO.IS","TOASO.IS","PETKM.IS","KOZAL.IS"
]

# 📈 SİNYAL KONTROL
def check(symbol):
    try:
        data = yf.download(symbol, period="3mo", interval="1d", progress=False)

        if data is None or data.empty:
            return False

        close = data["Close"]
        volume = data["Volume"]
        ema50 = close.ewm(span=50).mean()

        breakout = close.iloc[-1] > close.rolling(20).max().iloc[-2]
        trend = close.iloc[-1] > ema50.iloc[-1]
        vol = volume.iloc[-1] > volume.rolling(20).mean().iloc[-1]

        return breakout and trend and vol

    except:
        return False


# 🚀 ANA DÖNGÜ (7/24 çalışır)
while True:
    try:
        results = []

        for s in stocks:
            if check(s):
                results.append(s)

        if len(results) == 0:
            send("📊 BIST: Sinyal yok")
        else:
            send("📊 BIST Sinyal:\n" + "\n".join(results))

    except:
        send("⚠️ Bot hata verdi ama çalışmaya devam ediyor")

    time.sleep(600)  # 10 dakika
