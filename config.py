import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("APP_ENV", "development")

env_file = f"{env}.env"
if os.path.exists(env_file):
    load_dotenv(env_file)

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAIN_CHAT_ID = os.getenv("MAIN_CHAT_ID")
GIFT_CHAT_ID = os.getenv("GIFT_CHAT_ID")
FOLLOWERS_DATA_FILE = os.getenv("FOLLOWERS_DATA_FILE", "/data/followers.json")
BIRTHDAYS_DATA_FILE = os.getenv("BIRTHDAYS_DATA_FILE", "/data/birthdays.json")
TIMEZONES_DATA_FILE = os.getenv("TIMEZONES_DATA_FILE", "/data/timezones.json")
GIFT_PREP_DAYS = int(os.getenv("GIFT_PREP_DAYS", 3))
