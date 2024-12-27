import json
from datetime import datetime, UTC, date
from typing import NoReturn

from telebot import TeleBot

from config import MAIN_CHAT_ID, GIFT_CHAT_ID, GIFT_PREP_DAYS, BIRTHDAYS_DATA_FILE
from functions import get_mention


def check_birthday(bot: TeleBot) -> NoReturn:
    today = datetime.now(UTC).date()

    with open(BIRTHDAYS_DATA_FILE) as file:
        birthdays_data: dict[str, int] = json.load(file)

    for bday, uid in birthdays_data.items():
        birthday = date.fromisoformat(bday)
        
        delta = today - birthday.replace(year=today.year)
        years = today.year - birthday.year

        if delta.days >= 1:
            unban(bot, uid)
        elif delta.days == 0:
            congratulate(bot, uid, years)
        elif delta.days >= -GIFT_PREP_DAYS:
            ban(bot, uid, -delta.days, years)


def congratulate(bot: TeleBot, user_id: int, years: int) -> NoReturn:
    mention = get_mention(bot, user_id)

    gift_chat_message = f"У {mention} сегодня день рождения, не забудьте отправить подарки!"
    bot.send_message(GIFT_CHAT_ID, gift_chat_message, "HTML")

    if years % 5 == 0:
        main_chat_message0 = f"Поздравляю с днём рождения и {years}-летием, {mention}!"
    else:
        main_chat_message0 = f"С днём рождения, {mention}! Тебе уже {years} :)"

    main_chat_message1 = "\U0001F382"
    bot.send_message(MAIN_CHAT_ID, main_chat_message0, "HTML")
    bot.send_message(MAIN_CHAT_ID, main_chat_message1)


def ban(bot: TeleBot, user_id: int, prep_days: int, years: int) -> NoReturn:
    if bot.get_chat_member(GIFT_CHAT_ID, user_id).status == "kicked":
        return
    
    banned_successfully = bot.ban_chat_member(GIFT_CHAT_ID, user_id)

    if banned_successfully:
        mention = get_mention(bot, user_id)
        message = (f"Через {prep_days} дня у {mention} день рождения ({years} лет), поэтому я ЗАБАНИЛ его, чтобы вы "
                   f"смогли в тайне подготовить подарок. Удачи! :)")
        bot.send_message(GIFT_CHAT_ID, message, "HTML")


def unban(bot: TeleBot, user_id: int) -> NoReturn:
    if bot.get_chat_member(GIFT_CHAT_ID, user_id).status != "kicked":
        return
    
    unbanned_successfully = bot.unban_chat_member(GIFT_CHAT_ID, user_id)

    if unbanned_successfully:
        mention = get_mention(bot, user_id)
        message = f"{mention} отметил день рождения и теперь разбанен."
        bot.send_message(GIFT_CHAT_ID, message, "HTML")
