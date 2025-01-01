import json
from datetime import datetime, UTC, date

import schedule
from telebot import TeleBot

from config import MAIN_CHAT_ID, TIMEZONES_DATA_FILE
from functions import get_mention


def check_new_year(bot: TeleBot) -> None:
    today = datetime.now(UTC).date()
    if today != date(year=today.year, month=12, day=31):
        return
    
    with open(TIMEZONES_DATA_FILE) as file:
        timezones_data: dict[str, list[int]] = json.load(file)
    
    for tz, uids in timezones_data.items():
        schedule.every().day.at("00:00", tz).do(congratulate, bot=bot, user_ids=uids)


def congratulate(bot: TeleBot, user_ids: list[int]):
    mentions: list[str] = []
    for uid in user_ids:
        mention = get_mention(bot, uid)
        if mention is not None:
            mentions.append(mention)

    if not mentions:
        return schedule.CancelJob
    
    message0 = f"С НОВЫМ ГОДОМ, {", ".join(mentions)}!"
    message1 = "\U0001F389"
    
    bot.send_message(MAIN_CHAT_ID, message0, "HTML")
    bot.send_message(MAIN_CHAT_ID, message1)

    return schedule.CancelJob
