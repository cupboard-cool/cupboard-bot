from flask import Flask, request, jsonify
import functions, messages, config

from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

URL = f'https://api.telegram.org/bot{config.token}/'

@app.route(f'/{config.token}', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            r = request.get_json()
            chat_id = r['message']['chat']['id']
            chat_type = r['message']['chat']['type']

            if 'text' in r['message']:
                message = r['message']['text']
                for symbol in messages.forbidden:
                    if symbol in message: message = message.replace(symbol, "").lower()
                message_words = message.split(' ')
            else:
                message = ' '

            if 'username' in r['message']['from']:
                username = r['message']['from']['username']
            else:
                username = 'unknown'

            functions.process_commands(message, chat_id, username, chat_type)
            print(message, chat_id, username, message_words, chat_type)
            functions.process_message(message, chat_id, username, message_words, chat_type)

        except:
            pass

        return jsonify(r)
    return '<h1>Trybot is working!</h1>'

@app.route(f"/{config.key}", methods=['POST'])
def notify():
    try:
        r = request.get_json()
        message = r['message']
        functions.notify_followers(message)
    except:
        pass
    return 'A'

if __name__ == '__main__':
    app.run(debug=True)
