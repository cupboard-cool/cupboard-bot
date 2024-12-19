import json
from datetime import datetime, UTC, timedelta

from telebot import TeleBot

from config import MAIN_CHAT_ID, GIFT_CHAT_ID, GIFT_PREP_DAYS


def check_birthday(bot: TeleBot, date_format: str, birthdays_file: str) -> None:
    today = datetime.now(UTC).date()

    today_birthday = today.strftime(date_format)
    upcoming_birthday = (today + timedelta(days=GIFT_PREP_DAYS)).strftime(date_format)
    past_birthday = (today - timedelta(days=1)).strftime(date_format)

    with open(birthdays_file) as file:
        birthdays_list = json.load(file)
        birthdays = birthdays_list.keys()
    
    if (today_birthday in birthdays):
        congratulate(bot, birthdays_list[today_birthday])

    if (upcoming_birthday in birthdays):
        ban(bot, birthdays_list[upcoming_birthday])

    if (past_birthday in birthdays):
        unban(bot, birthdays_list[past_birthday])


def congratulate(bot: TeleBot, id: str) -> None:
    username = bot.get_chat(id).username

    gift_chat_message = f"У @{username} сегодня день рождения, не забудьте отправить подарки!"
    bot.send_message(GIFT_CHAT_ID, gift_chat_message)

    main_chat_message0 = f"С днём рождения, @{username}!"
    main_chat_message1 = "\U0001F382"
    bot.send_message(MAIN_CHAT_ID, main_chat_message0)
    bot.send_message(MAIN_CHAT_ID, main_chat_message1)


def ban(bot: TeleBot, id: str) -> None:
    banned = bot.ban_chat_member(GIFT_CHAT_ID, id)

    if banned:
        username = bot.get_chat(id).username
        message = f"Через {GIFT_PREP_DAYS} дня у @{username} день рождения, поэтому я ЗАБАНИЛ его, чтобы вы смогли в тайне подготовить подарок. Удачи! :)"
        bot.send_message(GIFT_CHAT_ID, message)


def unban(bot: TeleBot, id: str) -> None:
    unbanned = bot.unban_chat_member(GIFT_CHAT_ID, id)

    if unbanned:
        username = bot.get_chat(id).username
        message = f"@{username} отметил день рождения и теперь разбанен."
        bot.send_message(GIFT_CHAT_ID, message)
