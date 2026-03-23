# AI News Mailer 🚀

## 📌 Overview
This project automatically fetches the latest AI news and sends a daily email summary.

## ⚙️ Tech Stack
- Python
- GNews API
- SMTP (Email)
- GitHub Actions

## 🔄 How it works
1. Fetch news from GNews API
2. Select top 5 articles
3. Format them into a summary
4. Send email using SMTP

## ⏰ Automation
This project runs daily using GitHub Actions (scheduled workflow).

## 🔐 Environment Variables
Add the following secrets:

- NEWS_API_KEY
- SENDER_EMAIL
- APP_PASSWORD
- RECEIVER_EMAIL

## ▶️ Run Locally
```bash
pip install -r requirements.txt
python app.py
