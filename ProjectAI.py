import requests
# from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import schedule
import time
from datetime import datetime, timedelta
import os

NEWS_API_KEY = os.getenv("a92fa6fc0de9443f94f7f6f43534545b")
SENDER_EMAIL = os.getenv("kalyanbandaru11@gmail.com")
APP_PASSWORD = os.getenv("elzh wfbd ztsc hnfp")
RECEIVER_EMAIL = os.getenv("bandarukalyan1107@gmail.com")

# ===================== CONFIG =====================



SEND_TIME = "09:00"   # daily time

# ==================================================

#client = OpenAI(api_key=OPENAI_API_KEY)


def get_news():
    url = (
        "https://newsapi.org/v2/everything?"
        "q=AI OR artificial intelligence"
        "&sortBy=publishedAt"
        "&language=en"
        "&pageSize=10"
        f"&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])

    news_list = []
    for article in articles:
        title = article.get("title")
        description = article.get("description")

        # skip bad/empty data
        if not title or not description:
            continue

        news_list.append(f"{title} - {description}")

        # stop when we reach 5
        if len(news_list) == 5:
            break

    return news_list

def summarize_news(news_list):
    news_text = "\n".join(news_list)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Give me 5 clear bullet points of latest AI news:\n{news_text}"
            }
        ]
    )

    return response.choices[0].message.content


def send_email(content):
    msg = MIMEText(content)
    msg["Subject"] = "Daily AI News (Last 24 Hours)"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()


def format_news(news_list):
    content = "🧠 Daily AI News (Last 24 Hours)\n\n"

    for i, news in enumerate(news_list, 1):
        content += f"{i}. {news}\n\n"

    content += "\n-- End of Report --"
    return content


def job():
    print("Running AI news job...")

    try:
        news = get_news()
        if not news:
            print("No news found")
            return

        summary = format_news(news)
        send_email(summary)

        print("Email sent successfully!")

    except Exception as e:
        print("Error:", e)


# Schedule
if __name__ == "__main__":
    job()