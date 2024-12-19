import configparser

from os.path import isfile


def create_config(config_path):
    config = configparser.ConfigParser()

    config['General'] = {
        'debug': True,
        'key': ''
    }
    config['Bot'] = {
        'token': '',
        'debug_token': ''
    }
    config['Files'] = {
        'followers_data': 'followers.json'
    }

    with open(config_path, 'w') as configfile:
        config.write(configfile)


def read_config(config_path):
    config = configparser.ConfigParser()

    config.read(config_path)

    debug_mode = config.getboolean('General', 'debug')

    key = config.get('General', 'key')
    bot_token = config.get('Bot', 'debug_token') if debug_mode \
        else config.get('Bot', 'token')

    followers_data_file = config.get('Files', 'followers_data')

    config_vals = {
        'debug_mode': debug_mode,
        'key': key,
        'followers_data_file': followers_data_file,
        'bot_token': bot_token
    }

    return config_vals


config_file = 'config.ini'

if not isfile(config_file):
    create_config(config_file)

config_values = read_config(config_file)

DEBUG_MODE = config_values['debug_mode']
KEY = config_values['key']
BOT_TOKEN = config_values['bot_token']
FOLLOWERS_DATA_FILE = config_values['followers_data_file']
