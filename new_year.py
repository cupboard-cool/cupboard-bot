import json
from datetime import datetime, UTC, date
from typing import NoReturn

from telebot import TeleBot

from config import MAIN_CHAT_ID, TIMEZONES_DATA_FILE
from functions import get_mention


def check_new_year(bot: TeleBot) -> NoReturn:
    raise NotImplementedError
