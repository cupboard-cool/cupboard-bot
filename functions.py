from random import choice, randrange
import difflib
import messages
import json

from main import bot



def notify_followers(message):
    with open('bot/followers.json') as followers_data:
        followers = json.load(followers_data)['followers']
        for follower in followers:
            bot.sendMessage(follower['chat_id'], message)



def process_commands(message, chat_id, username, chat_type):
    if '/try' in message:
        s = message.split(' ', 1)
        action = s[1]
        for exception in messages.exceptions_list:
            if action == exception:
                message_respone = "У {0}, получилось {1}".format(username, action)
                break
        else:
            randnum = randrange(1,100,1)
            if randnum > 50:
                message_respone = "У {0}, получилось {1}".format(username, action)
            else:
                message_respone = "У {0}, не получилось {1}".format(username, action)
        bot.sendMessage(chat_id, message_respone)

    if chat_type == 'private':

        if message == '/follow':
                with open('bot/followers.json') as followers_data:
                    data = json.load(followers_data)
                for follower in data['followers']:
                    if follower['chat_id'] == chat_id:
                        message_respone = "Асыбка! Вы узе падписаны на апавесенние."
                        break
                else:
                    data["followers"].append({
                        'chat_id':  chat_id
                    })
                    with open('bot/followers.json', 'w') as followers_data:
                        json.dump(data, followers_data)
                    message_respone = "Вы успесна падписались на апавесенние."
                bot.sendMessage(chat_id, message_respone)

        if message == '/unfollow':
            with open('bot/followers.json') as followers_data:
                data = json.load(followers_data)
            for follower in data['followers']:
                if follower['chat_id'] == chat_id:
                    data['followers'].remove({'chat_id': chat_id})
                    with open('bot/followers.json', 'w') as followers_data:
                        json.dump(data, followers_data)
                    message_respone = "Вы успесна атписались ат апавесенния."
                    break
            else:
                message_respone = "Асыбка! Вы исё не падписаны на апавесенние."
            bot.sendMessage(chat_id, message_respone)



def process_message(message, chat_id, username, message_words, chat_type):
    loopbreak = False
    if chat_type == 'private':
        for trigger_message_dictionary in messages.trigger_message_dictionaries_list:
                for trigger_message_array_obj in trigger_message_dictionary['trigger_message_array']:
                    any_result = [trigger_message_array_obj in message.lower(),
                                  difflib.get_close_matches(message.lower(), trigger_message_dictionary['trigger_message_array'], n=1, cutoff=0.7)]
                    if any(any_result):
                        bot.sendMessage(chat_id, choice(trigger_message_dictionary['respone_message_array']).format(username))
                        loopbreak = True
                        break
                if loopbreak:
                    break
    else:
        for name_trigger in messages.name_triggers:
            if (difflib.get_close_matches(name_trigger, message_words)) or (name_trigger in message_words):
                for trigger_message_dictionary in messages.trigger_message_dictionaries_list:
                    for trigger_message_array_obj in trigger_message_dictionary['trigger_message_array']:
                        any_result = [trigger_message_array_obj in message.lower(),
                                    difflib.get_close_matches(message.lower(), trigger_message_dictionary['trigger_message_array'], n=1, cutoff=0.7)]
                        if any(any_result):
                            bot.sendMessage(chat_id, choice(trigger_message_dictionary['respone_message_array']).format(username))
                            loopbreak = True
                            break
                    if loopbreak:
                        break
            if loopbreak:
                break

    for nontarget_trigger_message_dictionary in messages.nontarget_trigger_message_dictionaries_list:
        for nontarget_message_array_obj in nontarget_trigger_message_dictionary['trigger_message_array']:
            nontarget_any_result = [nontarget_message_array_obj in message.lower(),
                                    difflib.get_close_matches(message.lower(), nontarget_trigger_message_dictionary['trigger_message_array'], cutoff=0.7)]
            if any(nontarget_any_result):
                bot.sendMessage(chat_id, choice(nontarget_trigger_message_dictionary['respone_message_array']).format(username))
                loopbreak = True
                break
        if loopbreak:
            break