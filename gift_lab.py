from datetime import datetime, UTC, timedelta
import json


def check_birthday(date_format: str, birthdays_file: str) -> None:
    today = datetime.now(UTC).date()

    today_birthday = today.strftime(date_format)
    upcoming_birthday = (today + timedelta(days=3)).strftime(date_format)
    past_birthday = (today - timedelta(days=1)).strftime(date_format)

    with open(birthdays_file) as file:
        birthdays_list = json.load(file)
        birthdays = birthdays_list.keys()
    
    if (today_birthday in birthdays):
        congratulate(birthdays_list[today])

    if (upcoming_birthday in birthdays):
        ban(birthdays_list[upcoming_birthday])

    if (past_birthday in birthdays):
        unban(birthdays_list[past_birthday])


def congratulate(id: str) -> None:
    raise NotImplementedError


def ban(id: str) -> None:
    raise NotImplementedError


def unban(id: str) -> None:
    raise NotImplementedError