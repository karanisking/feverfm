import requests
import time
from datetime import datetime, timedelta

API_URL = "https://api.playwithfever.com/v1/contest/list/happening-quiz"
BOT_TOKEN = "8406747669:AAGczfXwFiHS8jiEEkCTDEfsD2HL1kIKxZI"
CHAT_ID = "1243736325"

# Track contest IDs you've already sent
seen_contests = set()

def format_datetime(dt_str):
    """Convert UTC datetime string to IST and format nicely."""
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    ist_time = dt + timedelta(hours=5, minutes=30)
    return ist_time.strftime("%d %B %Y, %I:%M %p")  # Example: 09 October 2025, 02:55 PM

def send_telegram_message(text, photo_url=None):
    """Send a message or photo to Telegram."""
    try:
        if photo_url:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            data = {"chat_id": CHAT_ID, "caption": text, "photo": photo_url}
            requests.post(url, data=data)
        else:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {"chat_id": CHAT_ID, "text": text}
            requests.post(url, data=data)
    except Exception as e:
        print("Telegram send error:", e)

def check_new_contests():
    """Check for new contests and send alerts for new ones."""
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

                # Use thumbnail instead of full image
                send_telegram_message(message, photo_url=game.get('contest_thumb'))

    except Exception as e:
        print("Error:", e)

# Check every 5 minutes
if __name__ == "__main__":
    print("🤖 Fever Bot started! Checking for new contests every 5 minutes...")
    while True:
        check_new_contests()
        time.sleep(300)
