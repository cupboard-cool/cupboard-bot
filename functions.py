from random import choice, random
from difflib import get_close_matches
import json

import messages
import config

from config import bot



def notify_followers(message):
    with open(config.followers_data_path) as followers_data:
        followers = json.load(followers_data)['followers']
        for follower in followers:
            bot.send_message(follower['chat_id'], message)



def process_command(message, chat_id, username, chat_type):
    command = message.split(' ', 1)[0]
    arg = message.split(' ', 1)[1] if len(message.split(' ')) > 1 else None

    if command == '/try':
        for exception in messages.exceptions_list:
            if arg == exception['text']:
                message_response = "У {0}, получилось {1}".format(username, arg) if exception['answer'] else "У {0}, не получилось {1}".format(username, arg)
                break
        else:
            if random() > 0.5:
                message_response = "У {0}, получилось {1}".format(username, arg)
            else:
                message_response = "У {0}, не получилось {1}".format(username, arg)

        bot.send_message(chat_id, message_response)

    if chat_type == 'private':
        if command == '/follow':
                data = None

                try:
                    with open(config.followers_data_path) as followers_data:
                        data = json.load(followers_data)

                    for follower in data['followers']:
                        if follower['chat_id'] == chat_id:
                            message_response = messages.error_follow_response
                            break
                    else:
                        data["followers"].append({'chat_id': chat_id})

                        with open(config.followers_data_path, 'w') as followers_data:
                            json.dump(data, followers_data)

                        message_response = messages.successful_follow_response
                except:
                    pass

                if data == None:
                    with open(config.followers_data_path, 'w') as followers_data:
                        json.dump({"followers": [{'chat_id': chat_id}]}, followers_data)
                        message_response = messages.successful_follow_response

                bot.send_message(chat_id, message_response)

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

                        message_response = messages.successful_unfollow_response
                        break
                else:
                    message_response = messages.error_unfollow_response
            except:
                pass

            if data == None:
                with open(config.followers_data_path, 'w') as followers_data:
                    json.dump({"followers": []}, followers_data)
                    message_response = messages.error_unfollow_response

            bot.send_message(chat_id, message_response)



def process_message(message, chat_id, username, message_words, chat_type):
    for trigger_message_dictionary in messages.trigger_message_dictionaries_list:
        trigger_matches = [trigger_message_array_obj for trigger_message_array_obj in trigger_message_dictionary['trigger_message_array'] if trigger_message_array_obj in message.lower()]
        close_trigger_matches = get_close_matches(message.lower(), trigger_message_dictionary['trigger_message_array'], n=1, cutoff=0.7)

        if trigger_matches or close_trigger_matches:
            if chat_type == 'private':
                bot.send_message(chat_id, choice(trigger_message_dictionary['response_message_array']).format(username))
                break
            else:
                name_trigger_matches = [name_trigger for name_trigger in messages.name_triggers if name_trigger in message_words]
                close_name_trigger_matches = [get_close_matches(name_trigger, message_words) for name_trigger in messages.name_triggers if get_close_matches(name_trigger, message_words)]

                if name_trigger_matches or close_name_trigger_matches:
                    bot.send_message(chat_id, choice(trigger_message_dictionary['response_message_array']).format(username))
                    break
    else:
        for nontarget_trigger_message_dictionary in messages.nontarget_trigger_message_dictionaries_list:
            trigger_matches = [{'text': trigger_message_array_obj, 'action': nontarget_trigger_message_dictionary['action']} for trigger_message_array_obj in nontarget_trigger_message_dictionary['trigger_message_array'] if trigger_message_array_obj in message.lower()]
            close_trigger_matches = get_close_matches(message.lower(), nontarget_trigger_message_dictionary['trigger_message_array'], n=1, cutoff=0.7)

            if trigger_matches or close_trigger_matches:
                if trigger_matches[0]['action'] != 'sneeze':
                    bot.send_message(chat_id, choice(nontarget_trigger_message_dictionary['response_message_array']).format(username))
                    break
                elif get_close_matches(message.lower(), nontarget_trigger_message_dictionary['trigger_message_array'], n=1, cutoff=1):
                    bot.send_message(chat_id, choice(nontarget_trigger_message_dictionary['response_message_array']).format(username))
                    break