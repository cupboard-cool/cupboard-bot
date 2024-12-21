import json
from datetime import datetime, UTC, date

from telebot import TeleBot

from config import MAIN_CHAT_ID, GIFT_CHAT_ID, GIFT_PREP_DAYS, BIRTHDAYS_DATA_FILE


def check_birthday(bot: TeleBot) -> None:
    today = datetime.now(UTC).date()

    with open(BIRTHDAYS_DATA_FILE) as file:
        birthdays_data: dict[str, str] = json.load(file)

    for bday, uid in birthdays_data.items():
        birthday = date.fromisoformat(bday)
        
        delta = today - birthday.replace(year=today.year)

        if delta.days >= 1:
            unban(bot, uid)
        elif delta.days == 0:
            congratulate(bot, uid, birthday)
        elif delta.days >= -GIFT_PREP_DAYS:
            ban(bot, uid)


def congratulate(bot: TeleBot, id: str, birthday: date) -> None:
    mention = get_mention(bot, id)

    gift_chat_message = f"У {mention} сегодня день рождения, не забудьте отправить подарки\\!"
    bot.send_message(GIFT_CHAT_ID, gift_chat_message, "MarkdownV2")

    main_chat_message0 = f"С днём рождения, {mention}\\!"
    main_chat_message1 = "\U0001F382"
    bot.send_message(MAIN_CHAT_ID, main_chat_message0, "MarkdownV2")
    bot.send_message(MAIN_CHAT_ID, main_chat_message1)


def ban(bot: TeleBot, id: str) -> None:
    banned = bot.ban_chat_member(GIFT_CHAT_ID, id)

    if banned:
        mention = get_mention(bot, id)
        message = f"Через {GIFT_PREP_DAYS} дня (или меньше) у {mention} день рождения, поэтому я ЗАБАНИЛ его, чтобы вы смогли в тайне подготовить подарок. Удачи\\! :)"
        bot.send_message(GIFT_CHAT_ID, message, "MarkdownV2")


def unban(bot: TeleBot, id: str) -> None:
    unbanned = bot.unban_chat_member(GIFT_CHAT_ID, id)

    if unbanned:
        mention = get_mention(bot, id)
        message = f"{mention} отметил день рождения и теперь разбанен."
        bot.send_message(GIFT_CHAT_ID, message, "MarkdownV2")


def get_mention(bot: TeleBot, id: str) -> str:
    chat_info = bot.get_chat(id)

    username = chat_info.username

    if username is not None:
        mention = f"@{username}"
    else:
        mention = f"[{chat_info.first_name}](tg://user?id={id})"

    return mention