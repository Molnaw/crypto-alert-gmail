import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def get_bitkub_price(symbol):
    try:
        url = "https://api.bitkub.com/api/market/ticker"
        response = requests.get(url)
        data = response.json()
        return data.get(f"THB_{symbol}", {}).get("last", "N/A")
    except:
        return "Error"

def get_okx_price(symbol):
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT"
        response = requests.get(url)
        data = response.json()
        return data['data'][0]['last']
    except:
        return "Error"

def send_email(subject, body):
    sender_email = os.environ.get('GMAIL_USER')
    receiver_email = os.environ.get('GMAIL_USER')
    password = os.environ.get('GMAIL_APP_PASSWORD')

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# รายการเหรียญที่ต้องการตรวจสอบ
coins = ["BTC", "ETH", "SOL"]
report = "--- Crypto Price Report ---\n\n"

for coin in coins:
    bk_price = get_bitkub_price(coin)
    ok_price = get_okx_price(coin)
    report += f"🪙 {coin}:\nBitkub: {bk_price} THB\nOKX: {ok_price} USDT\n\n"

send_email("Crypto Price Alert", report)
