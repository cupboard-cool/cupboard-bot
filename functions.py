from random import getrandbits
import json
from typing import Optional

import messages
from config import *


def try_todo(action: Optional[str]) -> bool:
    for exception in messages.exceptions_list:
        if action == exception['text']:
            return exception['answer']

    return bool(getrandbits(1))


def follow_notifications(user_id: str) -> str:
    data = {}

    try:
        with open(FOLLOWERS_DATA_FILE) as followers_data:
            data = json.load(followers_data)

        if user_id in [follower['user_id'] for follower in data['followers']]:
            return messages.error_follow_response
    except FileNotFoundError:
        pass

    try:
        len(data['followers'])
    except KeyError:
        data['followers'] = []

    data["followers"].append({'user_id': user_id})

    with open(FOLLOWERS_DATA_FILE, 'w') as followers_data:
        json.dump(data, followers_data)

    return messages.successful_follow_response


def unfollow_notifications(user_id: str) -> str:
    data = {}

    try:
        with open(FOLLOWERS_DATA_FILE) as followers_data:
            data = json.load(followers_data)

        if user_id in [follower['user_id'] for follower in data['followers']]:
            data['followers'].remove({'user_id': user_id})

            with open(FOLLOWERS_DATA_FILE, 'w') as followers_data:
                json.dump(data, followers_data)

            return messages.successful_unfollow_response

        return messages.error_unfollow_response
    except FileNotFoundError:
        data['followers'] = []

        with open(FOLLOWERS_DATA_FILE, 'w') as followers_data:
            json.dump(data, followers_data)

        return messages.error_unfollow_response
