from flask import Flask, request
import telegram
import schedule
import threading
import time

import functions
import messages
from config import bot, key, token, birthdays_file
import birthday

from flask_sslify import SSLify


def run_continuously(interval=60):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

schedule.every().day.at("06:00", "utc").do(birthday.check_birthday, "%Y-%m-%d", birthdays_file)
stop_run_continuously = run_continuously()

app = Flask(__name__)
sslify = SSLify(app)


@app.route(f'/{token}', methods=['POST'])
def index():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        chat_type = update.message.chat.type

        msg_text = update.message.text.encode('utf-8').decode()

        for symbol in messages.forbidden:
            if symbol in msg_text: msg_text = msg_text.replace(symbol, "").lower()
        msg_words = msg_text.split(' ')

        username = update.message.from_user.username if update.message.from_user.username else 'unknown'

        print(msg_text, chat_id, username, msg_words, chat_type)
        functions.process_command(msg_text, chat_id, username, chat_type)
        functions.process_message(msg_text, chat_id, username, msg_words, chat_type)
    except:
        pass
    return 'A'


@app.route(f"/{key}", methods=['POST'])
def notify():
    try:
        r = request.get_json()
        message = r['message']
        functions.notify_followers(message)
    except:
        pass
    return 'B'

if __name__ == '__main__':
    app.run(debug=True)
    stop_run_continuously.set()
