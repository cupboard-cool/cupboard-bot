from random import choice, random
from difflib import get_close_matches
import json

import messages
import config

from main import bot



def notify_followers(message):
    with open(config.followers_data_path) as followers_data:
        followers = json.load(followers_data)['followers']
        for follower in followers:
            bot.send_message(follower['chat_id'], message)



def process_command(message, chat_id, username, chat_type):
    command = message.split(' ', 1)[0]
    arg = message.split(' ', 1)[1] if len(message.split(' ')) > 1 else None

    if command == '/try':
        if arg in messages.exceptions_list:
            message_respone = "У {0}, получилось {1}".format(username, arg)
        elif random() > 0.5:
            message_respone = "У {0}, получилось {1}".format(username, arg)
        else:
            message_respone = "У {0}, не получилось {1}".format(username, arg)

        bot.send_message(chat_id, message_respone)

    if chat_type == 'private':
        if command == '/follow':
                data = None

                try:
                    with open(config.followers_data_path) as followers_data:
                        data = json.load(followers_data)

                    for follower in data['followers']:
                        if follower['chat_id'] == chat_id:
                            message_respone = "Асыбка! Вы узе падписаны на апавесенние."
                            break
                    else:
                        data["followers"].append({'chat_id': chat_id})

                        with open(config.followers_data_path, 'w') as followers_data:
                            json.dump(data, followers_data)

                        message_respone = "Вы успесна падписались на апавесенние."
                except:
                    pass

                if data == None:
                    with open(config.followers_data_path, 'w') as followers_data:
                        json.dump({"followers": [{'chat_id': chat_id}]}, followers_data)
                        message_respone = "Вы успесна падписались на апавесенние."

                bot.send_message(chat_id, message_respone)

        if command == '/unfollow':
            data = None

            try:
                with open(config.followers_data_path) as followers_data:
                    data = json.load(followers_data)

                for follower in data['followers']:
                    if follower['chat_id'] == chat_id:
                        data['followers'].remove({'chat_id': chat_id})

                        with open(config.followers_data_path, 'w') as followers_data:
                            json.dump(data, followers_data)

                        message_respone = "Вы успесна атписались ат апавесенния."
                        break
                else:
                    message_respone = "Асыбка! Вы исё не падписаны на апавесенние."
            except:
                pass

            if data == None:
                with open(config.followers_data_path, 'w') as followers_data:
                    json.dump({"followers": []}, followers_data)
                    message_respone = "Асыбка! Вы исё не падписаны на апавесенние."

            bot.send_message(chat_id, message_respone)



def process_message(message, chat_id, username, message_words, chat_type):
    for trigger_message_dictionary in messages.trigger_message_dictionaries_list:
        trigger_matches = [trigger_message_array_obj for trigger_message_array_obj in trigger_message_dictionary['trigger_message_array'] if trigger_message_array_obj in message.lower()]
        close_trigger_matches = get_close_matches(message.lower(), trigger_message_dictionary['trigger_message_array'], n=1, cutoff=0.7)

        if trigger_matches or close_trigger_matches:
            if chat_type == 'private':
                bot.send_message(chat_id, choice(trigger_message_dictionary['respone_message_array']).format(username))
                break
            else:
                name_trigger_matches = [name_trigger for name_trigger in messages.name_triggers if name_trigger in message_words]
                close_name_trigger_matches = [get_close_matches(name_trigger, message_words) for name_trigger in messages.name_triggers if get_close_matches(name_trigger, message_words)]
                
                if name_trigger_matches or close_name_trigger_matches:
                    bot.send_message(chat_id, choice(trigger_message_dictionary['respone_message_array']).format(username))
                    break
    else:
        for nontarget_trigger_message_dictionary in messages.nontarget_trigger_message_dictionaries_list:
            trigger_matches = [trigger_message_array_obj for trigger_message_array_obj in nontarget_trigger_message_dictionary['trigger_message_array'] if trigger_message_array_obj in message.lower()]
            close_trigger_matches = get_close_matches(message.lower(), nontarget_trigger_message_dictionary['trigger_message_array'], n=1, cutoff=0.7)

            if trigger_matches or close_trigger_matches:
                bot.send_message(chat_id, choice(nontarget_trigger_message_dictionary['respone_message_array']).format(username))
                break