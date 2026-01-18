name: Crypto Daily Alert

on:
  schedule:
    # รอบที่ 1: 07:00 น. เวลาไทย
    - cron: '0 0 * * *'
    # รอบที่ 2: 12:00 น. เวลาไทย
    - cron: '0 5 * * *'
    # รอบที่ 3: 19:00 น. เวลาไทย
    - cron: '0 12 * * *'
  workflow_dispatch:

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install requests

      - name: Run Alert Bot
        env:
          GMAIL_USER: ${{ secrets.GMAIL_USER }}
          GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
        run: python crypto_alert.py
