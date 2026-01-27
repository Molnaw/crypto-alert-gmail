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

def get_bitkub_price(symbol):
    try:
        url = "https://api.bitkub.com/api/market/ticker"
        response = requests.get(url)
        data = response.json()
        return float(data[f'THB_{symbol}']['last'])
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

# --- ข้อมูลพอร์ต OKX (อัปเดตตามรูปของคุณ) ---
okx_assets = {
    'USDT': 3.91333774,
    'BTC': 0.0000376,
    'OKB': 0.00000024
}

# --- ข้อมูลพอร์ต Bitkub (อัปเดตตามรูปของคุณ) ---
bitkub_assets = {
    'KUB': 3.13398582,
    'BNB': 0.00419117
}

# ดึงราคาล่าสุด
btc_price_usd = get_okx_price('BTC')
okb_price_usd = get_okx_price('OKB')
kub_price_thb = get_bitkub_price('KUB')
bnb_price_thb = get_bitkub_price('BNB')

# คำนวณมูลค่า OKX (USD)
btc_val = okx_assets['BTC'] * btc_price_usd if btc_price_usd else 0
okb_val = okx_assets['OKB'] * okb_price_usd if okb_price_usd else 0
total_okx_usd = okx_assets['USDT'] + btc_val + okb_val

# คำนวณมูลค่า Bitkub (THB)
kub_val = bitkub_assets['KUB'] * (kub_price_thb if kub_price_thb else 0)
bnb_val = bitkub_assets['BNB'] * (bnb_price_thb if bnb_price_thb else 0)
total_bitkub_thb = kub_val + bnb_val

# สร้างเนื้อหารายงาน
report = "📢 รายงานพอร์ตคริปโตรายวัน (OKX & Bitkub)\n\n"

report += "🌐 [พอร์ต OKX]\n"
report += f"💰 มูลค่ารวม: ${total_okx_usd:.2f} USD\n"
report += f"💵 USDT: {okx_assets['USDT']:.2f}\n"
report += f"₿ BTC: {okx_assets['BTC']} (ราคา ${btc_price_usd:,.0f})\n"
report += f"🔸 OKB: {okx_assets['OKB']}\n\n"

report += "🇹🇭 [พอร์ต Bitkub]\n"
report += f"💰 มูลค่ารวม: {total_bitkub_thb:.2f} THB\n"
report += f"🟢 KUB: {bitkub_assets['KUB']:.4f} (ราคา {kub_price_thb} บาท)\n"
report += f"🟡 BNB: {bitkub_assets['BNB']:.6f} (ราคา {bnb_price_thb:,.0f} บาท)\n"

if btc_price_usd and btc_price_usd > 85000:
    report += "\n🚀 แจ้งเตือน: ราคา BTC สูงกว่า $85,000 แล้ว!"

send_email("Crypto Portfolio Update (OKX & Bitkub)", report)
