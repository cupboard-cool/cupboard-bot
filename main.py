from flask import Flask, request
import telegram
import schedule

import functions
import messages
from config import bot, key, token
import gift_lab

from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

schedule.every().day.at("06:00", "utc").do(gift_lab.check_birthday("%Y-%m-%d", "cupboard_birthdays.json"))

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
