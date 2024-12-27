import json
from difflib import get_close_matches
from typing import Optional, NoReturn
from random import getrandbits

import telebot

import messages
from config import FOLLOWERS_DATA_FILE


def try_todo(action: Optional[str]) -> bool:
    for exception in messages.exceptions_list:
        if action == exception['text']:
            return exception['answer']

    return bool(getrandbits(1))


def follow_notifications(user_id: str) -> str:
    data = {}

    try:
        with open(FOLLOWERS_DATA_FILE) as followers_data:
            data = json.load(followers_data)

        if user_id in [follower['user_id'] for follower in data['followers']]:
            return messages.error_follow_response
    except FileNotFoundError:
        pass

    try:
        len(data['followers'])
    except KeyError:
        data['followers'] = []

    data["followers"].append({'user_id': user_id})

    with open(FOLLOWERS_DATA_FILE, 'w') as followers_data:
        json.dump(data, followers_data)

    return messages.successful_follow_response


def unfollow_notifications(user_id: str) -> str:
    data = {}

    try:
        with open(FOLLOWERS_DATA_FILE) as followers_data:
            data = json.load(followers_data)

        if user_id in [follower['user_id'] for follower in data['followers']]:
            data['followers'].remove({'user_id': user_id})

            with open(FOLLOWERS_DATA_FILE, 'w') as followers_data:
                json.dump(data, followers_data)

            return messages.successful_unfollow_response

        return messages.error_unfollow_response
    except FileNotFoundError:
        data['followers'] = []

        with open(FOLLOWERS_DATA_FILE, 'w') as followers_data:
            json.dump(data, followers_data)

        return messages.error_unfollow_response


def get_mention(bot: telebot.TeleBot, user_id: int) -> Optional[str]:
    try:
        chat_info = bot.get_chat(user_id)
        username = chat_info.username

        mention = f"@{username}" if username else f"<a href=\"tg://user?id={user_id}\">{chat_info.first_name}</a>"
        return mention
    except telebot.apihelper.ApiTelegramException:
        return None


def notify_followers(bot: telebot.TeleBot, message: str) -> NoReturn:
    followers = []

    try:
        with open(FOLLOWERS_DATA_FILE, 'r') as followers_data:
            followers = json.load(followers_data)['followers']
    except FileNotFoundError:
        with open(FOLLOWERS_DATA_FILE, 'x') as followers_data:
            json.dump({'followers': followers}, followers_data)

    if followers:
        for follower in followers:
            bot.send_message(follower['chat_id'], message)
    else:
        print('No followers')


def include_name_trigger(message: telebot.types.Message) -> bool:
    message_words = message.text.split()

    name_trigger_matches = [name_trigger for name_trigger in messages.name_triggers if
                            name_trigger in message_words]
    close_name_trigger_matches = [get_close_matches(name_trigger, message_words) for name_trigger in
                                  messages.name_triggers if get_close_matches(name_trigger, message_words)]

    return bool(name_trigger_matches) or bool(close_name_trigger_matches)
