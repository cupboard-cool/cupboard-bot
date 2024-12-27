import time
import threading
import sys
import json
from typing import NoReturn
from random import choice
from difflib import get_close_matches

import telebot
import schedule
from telebot import TeleBot, BaseMiddleware
from schedule import every, repeat
from kaomoji.kaomoji import Kaomoji

import messages
import functions
import birthday
from config import BOT_TOKEN, FOLLOWERS_DATA_FILE

try:
    bot = TeleBot(token=BOT_TOKEN, use_class_middlewares=True)
except ValueError:
    print('Bot token is invalid')
    sys.exit()


def schedule_run_continuously(interval=60) -> threading.Event:
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


@repeat(every().day.at("06:00", "utc"))
def process_day() -> NoReturn:
    birthday.check_birthday(bot)


class Middleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.update_types = ['message']

    def pre_process(self, message, data):
        for symbol in messages.forbidden:
            if message.text is not None and symbol in message.text:
                message.text = message.text.replace(symbol, "").lower()

    def post_process(self, message, data, exception=None):
        pass


bot.setup_middleware(Middleware())

kao = Kaomoji()


def notify_followers(message: str) -> NoReturn:
    try:
        with open(FOLLOWERS_DATA_FILE) as followers_data:
            followers = json.load(followers_data)['followers']
    except FileNotFoundError:
        followers = []

    if len(followers) == 0:
        print('No followers')
    else:
        for follower in followers:
            bot.send_message(follower['chat_id'], message)


@bot.message_handler(commands=['try'])
def try_command(message: telebot.types.Message) -> NoReturn:
    action = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else None
    username = message.from_user.username if message.from_user.username else 'unknown'

    if action is None:
        text = 'Что ты вообще пытаешься сделать? O.O'
    else:
        is_successfull = functions.try_todo(action)

        result = 'получилось' if is_successfull else 'не получилось'
        kao_categories = ['joy', 'love'] if is_successfull else ['indifference', 'sadness']

        kaomoji = kao.create(category=choice(kao_categories))
        text = f'У {username} {result} {action} {kaomoji}'

    bot.reply_to(message, text)


@bot.message_handler(commands=['follow'])
def follow_command(message: telebot.types.Message) -> NoReturn:
    user_id = str(message.from_user.id)
    response = functions.follow_notifications(user_id)

    bot.send_message(user_id, response)


@bot.message_handler(commands=['unfollow'])
def unfollow_command(message: telebot.types.Message) -> NoReturn:
    user_id = str(message.from_user.id)
    response = functions.unfollow_notifications(user_id)

    bot.send_message(user_id, response)


@bot.message_handler(func=lambda message: True)
def any_message(message: telebot.types.Message) -> NoReturn:
    username = message.from_user.username if message.from_user.username else 'unknown'
    message_text = message.text
    message_words = message_text.split(' ')
    chat_type = message.chat.type
    chat_id = message.chat.id

    for trigger_message_dictionary in messages.trigger_message_dictionaries_list:
        trigger_matches = [trigger_message_array_obj for trigger_message_array_obj in
                           trigger_message_dictionary['trigger_message_array'] if
                           trigger_message_array_obj in message_text.lower()]

        close_trigger_matches = get_close_matches(
            word=message_text.lower(),
            possibilities=trigger_message_dictionary['trigger_message_array'],
            n=1,
            cutoff=0.7
        )

        if trigger_matches or close_trigger_matches:
            if chat_type == 'private':
                bot.send_message(chat_id, choice(trigger_message_dictionary['response_message_array']).format(username))
                break
            else:
                name_trigger_matches = [name_trigger for name_trigger in messages.name_triggers if
                                        name_trigger in message_words]
                close_name_trigger_matches = [get_close_matches(name_trigger, message_words) for name_trigger in
                                              messages.name_triggers if get_close_matches(name_trigger, message_words)]

                if name_trigger_matches or close_name_trigger_matches:
                    bot.send_message(chat_id,
                                     choice(trigger_message_dictionary['response_message_array']).format(username))
                    break
    else:
        for nontarget_trigger_message_dictionary in messages.nontarget_trigger_message_dictionaries_list:
            trigger_matches = [
                {'text': trigger_message_array_obj, 'action': nontarget_trigger_message_dictionary['action']} for
                trigger_message_array_obj in nontarget_trigger_message_dictionary['trigger_message_array'] if
                trigger_message_array_obj in message_text.lower()]

            close_trigger_matches = get_close_matches(
                word=message_text.lower(),
                possibilities=nontarget_trigger_message_dictionary['trigger_message_array'],
                n=1,
                cutoff=0.7
            )

            if trigger_matches or close_trigger_matches:
                if trigger_matches[0]['action'] != 'sneeze':
                    bot.send_message(
                        chat_id=chat_id,
                        text=choice(nontarget_trigger_message_dictionary['response_message_array']).format(username)
                    )

                    break
                elif get_close_matches(
                        word=message_text.lower(),
                        possibilities=nontarget_trigger_message_dictionary['trigger_message_array'],
                        n=1,
                        cutoff=1
                ):

                    bot.send_message(
                        chat_id,
                        choice(nontarget_trigger_message_dictionary['response_message_array']).format(username))

                    break


def main() -> NoReturn:
    print("Program started.")
    stop_schedule_run = schedule_run_continuously()
    bot.infinity_polling()
    stop_schedule_run.set()


if __name__ == '__main__':
    main()
