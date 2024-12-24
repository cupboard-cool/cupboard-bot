# Cupboard Telegram Bot

![bot icon](icon.png)

## Description

A Telegram bot with various funny functions designed for small friend group chats. Examples include responses to pre-defined messages, a `/try` command that randomizes a result of a given action, and birthday greetings.

## How to build

### With Docker

1. Build the image using `docker build -t cupboard-bot .`.
2. Configure the `docker-compose.yml` file or pass your configuration directly to the container.
3. Run the container with `docker compose up` or `docker run cupboard-bot`.

### With Python 3.12.6

1. Install the requirements with `pip install -r requirements.txt`.
2. Create a `.env` file and populate it with environment variables. You can use multiple `.env` files for different environments, e.g. `development.env`, `production.env`.
3. Run `python main.py`.

## Environment variables (configuration)

`APP_ENV` - an environment where the bot runs, e.g. `development`, `production`. Default: `development`.  
`BOT_TOKEN` - a Telegram bot token.  
`MAIN_CHAT_ID` - an ID of a main chat, the bot will send greetings there.  
`GIFT_CHAT_ID` - an ID of a chat where users discuss gifts for upcoming birthdays. The user who has a birthday soon will be banned from this chat.  
`FOLLOWERS_DATA_FILE` - a path to a `.json` file with followers' data. Default: `/data/followers.json`.  
`BIRTHDAYS_DATA_FILE` - a path to a `.json` file with birthdays data, in the format `"iso_date": user_id`. Default: `/data/birthdays.json`.  
`GIFT_PREP_DAYS` - a number of days users in the gift chat have to make a present. The user who has a birthday in `GIFT_PREP_DAYS` days or less will be banned. Default: `3`.  
