from os.path import isfile
from configparser import ConfigParser


def create_config(config_path):
    config = ConfigParser()

    config['General'] = {
        'debug': 'True',
        'birthday_date_format': '%Y-%m-%d',
        'gift_prep_days': 3
    }
    config['Bot'] = {
        'token': '',
        'debug_token': ''
    }
    config['Files'] = {
        'followers_data': 'followers.json',
        'birthdays_data': 'birthdays.json'
    }
    config['Chats'] = {
        'main_chat_id': '',
        'gift_chat_id': ''
    }

    with open(config_path, 'w') as configfile:
        config.write(configfile)


def read_config(config_path):
    config = ConfigParser()

    config.read(config_path)

    debug_mode = config.getboolean('General', 'debug')

    bot_token = config.get('Bot', 'debug_token') if debug_mode \
        else config.get('Bot', 'token')

    followers_data_file = config.get('Files', 'followers_data')
    birthdays_data_file = config.get('Files', 'birthdays_data')
    main_chat_id = config.get('Chats', 'main_chat_id')
    gift_chat_id = config.get('Chats', 'gift_chat_id')
    birthday_date_format = config.get('General', 'birthday_date_format')
    gift_prep_days = config.getint('General', 'gift_prep_days')

    config_values = {
        'debug_mode': debug_mode,
        'bot_token': bot_token,
        'followers_data_file': followers_data_file,
        'birthdays_data_file': birthdays_data_file,
        'main_chat_id': main_chat_id,
        'gift_chat_id': gift_chat_id,
        'birthday_date_format': birthday_date_format,
        'gift_prep_days': gift_prep_days 
    }

    return config_values


config_file = 'config.ini'

if not isfile(config_file):
    create_config(config_file)

config_values = read_config(config_file)

DEBUG_MODE = config_values['debug_mode']
BOT_TOKEN = config_values['bot_token']
FOLLOWERS_DATA_FILE = config_values['followers_data_file']
BIRTHDAYS_DATA_FILE = config_values['birthdays_data_file']
MAIN_CHAT_ID = config_values['main_chat_id']
GIFT_CHAT_ID = config_values['gift_chat_id']
BIRTHDAY_DATE_FORMAT = config_values['birthday_date_format']
GIFT_PREP_DAYS = config_values['gift_prep_days']
