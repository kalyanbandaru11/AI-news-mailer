import requests
import smtplib
from email.mime.text import MIMEText
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# ===================== CONFIG =====================
SEND_TIME = "09:00"   # daily time
# ==================================================
def get_news():
    url = (
    "https://newsapi.org/v2/everything?"
    "q=AI OR artificial intelligence OR ChatGPT OR OpenAI"
    "&sortBy=publishedAt"
    "&language=en"
    "&pageSize=20"
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
        if not title:
            continue

        description = description or "No description available"

        news_list.append(f"{title} - {description}")

        # stop when we reach 5
        if len(news_list) == 5:
            break

    return news_list




def send_email(content):
    msg = MIMEText(content)
    msg["Subject"] = "Daily AI News (Last 24 Hours)"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
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
            print("No news found, sending fallback email")
            send_email("No major AI news found in the last 24 hours.")
            return

        summary = format_news(news)
        send_email(summary)

        print("Email sent successfully!")

    except Exception as e:
        print("Error:", e)


# Schedule
if __name__ == "__main__":
    job()
