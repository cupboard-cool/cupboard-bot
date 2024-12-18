from flask import Flask, request
import telegram
import schedule
from datetime import datetime
import json

import functions
import messages
import config

from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

bot = telegram.Bot(config.token)


def check_birthday():
    today = datetime.now(datetime.UTC)
    with open("cupboard_birthdays.json") as file:
        birthdays = json.load(file)

    upcoming_birthday = today + 3
    past_birthday = today - 1

    if (upcoming_birthday in birthdays.keys()):
        ban(birthdays[upcoming_birthday])

    if (past_birthday in birthdays.keys()):
        unban(birthdays[past_birthday])

    if (today in birthdays.keys()):
        congratulate()

schedule.every().day.at("06:00", "utc").do(check_birthday)

@app.route(f'/{config.token}', methods=['POST'])
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

@app.route(f"/{config.key}", methods=['POST'])
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
