import json
from datetime import datetime, UTC, date

from telebot import TeleBot

from config import MAIN_CHAT_ID, GIFT_CHAT_ID, GIFT_PREP_DAYS, BIRTHDAYS_DATA_FILE


def check_birthday(bot: TeleBot) -> None:
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


def congratulate(bot: TeleBot, id: int, years: int) -> None:
    mention = get_mention(bot, id)

    gift_chat_message = f"У {mention} сегодня день рождения, не забудьте отправить подарки!"
    bot.send_message(GIFT_CHAT_ID, gift_chat_message, "HTML")

    if years % 5 == 0:
        main_chat_message0 = f"Поздравляю с днём рождения и {years}-летием, {mention}!"
    else:
        main_chat_message0 = f"С днём рождения, {mention}! Тебе уже {years} :)"

    main_chat_message1 = "\U0001F382"
    bot.send_message(MAIN_CHAT_ID, main_chat_message0, "HTML")
    bot.send_message(MAIN_CHAT_ID, main_chat_message1)


def ban(bot: TeleBot, id: int, prep_days: int, years: int) -> None:
    if bot.get_chat_member(GIFT_CHAT_ID, id).status == "kicked":
        return
    
    banned_successfully = bot.ban_chat_member(GIFT_CHAT_ID, id)

    if banned_successfully:
        mention = get_mention(bot, id)
        message = f"Через {prep_days} дня у {mention} день рождения ({years} лет), поэтому я ЗАБАНИЛ его, чтобы вы смогли в тайне подготовить подарок. Удачи! :)"
        bot.send_message(GIFT_CHAT_ID, message, "HTML")


def unban(bot: TeleBot, id: int) -> None:
    if bot.get_chat_member(GIFT_CHAT_ID, id).status != "kicked":
        return
    
    unbanned_successfully = bot.unban_chat_member(GIFT_CHAT_ID, id)

    if unbanned_successfully:
        mention = get_mention(bot, id)
        message = f"{mention} отметил день рождения и теперь разбанен."
        bot.send_message(GIFT_CHAT_ID, message, "HTML")


def get_mention(bot: TeleBot, id: int) -> str:
    chat_info = bot.get_chat(id)

    username = chat_info.username

    if username is not None:
        mention = f"@{username}"
    else:
        mention = f"<a href=\"tg://user?id={id}\">{chat_info.first_name}</a>"

    return mention
