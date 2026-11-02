import os
import requests
from flask import Flask
import feedparser

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def fetch_financial_news():
    rss_url = "https://news.google.com/rss/search?q=หุ้นไทย+SET&hl=th&gl=TH&ceid=TH:th"
    feed = feedparser.parse(rss_url)
    news_list = []
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        news_list.append(f"- [{title}]({link})")
    return "\n".join(news_list)

@app.route("/")
def home():
    news_summary = fetch_financial_news()
    message = f"📢 **สรุปข่าวสารการเงินประจำวัน**\n\n{news_summary}"
    send_telegram_message(message)
    return "News Bot executed and sent message to Telegram successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
