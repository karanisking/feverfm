import requests
import time
import json
from datetime import datetime
import os

API_URL = "https://api.playwithfever.com/v1/contest/list/happening-quiz"
BOT_TOKEN = "8406747669:AAGczfXwFiHS8jiEEkCTDEfsD2HL1kIKxZI"
CHAT_ID = "1243736325"
SENT_FILE = "sent_contests.json"
LOG_FILE = "fever_bot.log"

# Manually maintained contest IDs that should never be sent again
seen_contests = {37, 43, 44, 45}  # add more IDs as needed

def save_sent_contests():
    # Save only new contests (for local tracking)
    with open(SENT_FILE, "w") as f:
        json.dump(list(seen_contests), f)

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")  # Also print to GitHub Actions log

def format_datetime(dt_str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return dt.strftime("%d %B %Y, %I:%M %p")  # e.g., 10 October 2025, 02:55 PM

def send_telegram_message(text, photo_url=None):
    try:
        if photo_url:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            data = {"chat_id": CHAT_ID, "caption": text, "photo": photo_url}
            requests.post(url, data=data)
        else:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {"chat_id": CHAT_ID, "text": text}
            requests.post(url, data=data)
        log_message(f"Sent message for contest: {text.splitlines()[1]}")  # ID line
    except Exception as e:
        log_message(f"Telegram send error: {e}")

def check_new_contests():
    global seen_contests
    try:
        response = requests.get(API_URL).json()
        active_games = response['data']['active_games']

        if not active_games:
            log_message("No active contests found.")

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

                send_telegram_message(message, photo_url=game['contest_thumb'])

        save_sent_contests()
        log_message("Check completed successfully.")

    except Exception as e:
        log_message(f"Error fetching contests: {e}")

if __name__ == "__main__":
    log_message("Fever Bot run started.")
    check_new_contests()
    log_message("Fever Bot run finished.\n")
