import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_okx_price(symbol):
    try:
        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT"
        response = requests.get(url)
        data = response.json()
        return float(data['data'][0]['last'])
    except:
        return None

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
    except Exception as e:
        print(f"Error: {e}")

# --- ข้อมูลพอร์ตของคุณ (อัปเดต 26 ม.ค. 2026) ---
assets = {
    'USDT': 3.91333774,
    'BTC': 0.0000376,
    'OKB': 0.00000024
}

btc_price = get_okx_price('BTC')
okb_price = get_okx_price('OKB')

# คำนวณมูลค่า
btc_value = assets['BTC'] * btc_price if btc_price else 0
okb_value = assets['OKB'] * okb_price if okb_price else 0
total_usd = assets['USDT'] + btc_value + okb_value

report = f"📢 รายงานพอร์ต OKX ล่าสุด\n"
report += f"💰 มูลค่ารวม: ${total_usd:.2f} USD\n\n"
report += f"💵 USDT: {assets['USDT']:.2f}\n"
report += f"₿ BTC: {assets['BTC']} (ราคา ${btc_price:,.0f})\n"
report += f"🔸 OKB: {assets['OKB']}\n"

if btc_price and btc_price > 75000:
    report += "\n🚀 แจ้งเตือน: BTC ทะลุ $75,000 แล้ว!"

send_email("OKX Portfolio Update", report)
