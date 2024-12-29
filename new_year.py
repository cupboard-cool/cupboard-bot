import json
from datetime import datetime, UTC, date
from typing import NoReturn

import schedule
from telebot import TeleBot

from config import MAIN_CHAT_ID, TIMEZONES_DATA_FILE
from functions import get_mention


def check_new_year(bot: TeleBot) -> NoReturn:
    today = datetime.now(UTC).date()
    if today != date(year=today.year, month=12, day=31):
        return
    
    with open(TIMEZONES_DATA_FILE) as file:
        timezones_data: dict[str, list[int]] = json.load(file)
    
    for tz, uids in timezones_data.items():
        schedule.every().day.at("00:00", tz).do(congratulate, bot=bot, user_ids=uids)


def congratulate(bot: TeleBot, user_ids: list[int]) -> NoReturn:
    raise NotImplementedError
