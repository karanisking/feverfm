import requests
import time
from datetime import datetime

API_URL = "https://api.playwithfever.com/v1/contest/list/happening-quiz"
BOT_TOKEN = "8406747669:AAGczfXwFiHS8jiEEkCTDEfsD2HL1kIKxZI"
CHAT_ID = "1243736325"

# Initial contest IDs you already know
seen_contests = {}

def format_datetime(dt_str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return dt.strftime("%d %B %Y, %I %p")  # e.g., 10 October 2025, 12 PM

def send_telegram_message(text, photo_url=None):
    if photo_url:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {"chat_id": CHAT_ID, "caption": text, "photo": photo_url}
        requests.post(url, data=data)
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": text}
        requests.post(url, data=data)

def check_new_contests():
    global seen_contests
    try:
        response = requests.get(API_URL).json()
        active_games = response['data']['active_games']

        for game in active_games:
            contest_id = int(game['contest_id'])
            if contest_id not in seen_contests:
                seen_contests.add(contest_id)

                start = format_datetime(game['start'])
                end = format_datetime(game['end'])

                message = (
                    f"🎉 New Contest!\n"
                    f"ID: {contest_id}\n"
                    f"Name: {game['contest_name']}\n"
                    f"Start: {start}\n"
                    f"End: {end}"
                )

                send_telegram_message(message, photo_url=game['contest_image'])

    except Exception as e:
        print("Error:", e)

# Check every 5 minutes
while True:
    check_new_contests()
    time.sleep(300)
