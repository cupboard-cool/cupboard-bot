# Cupboard Telegram Bot

![bot icon](icon.png)

## Description

A Telegram bot with various funny functions designed for small friend group chats. Examples include responses to
pre-defined messages, a `/try` command that randomizes a result of a given action, and birthday greetings.

## How to build for development

### With Docker

1. Create a `development.env` file and populate it with environment variables. You can use different `.env` files by
changing the `env_file` attribute in the `compose.yaml` file.
2. Run the application with `docker compose up --build`.

### With Python 3.12.6

1. Install the requirements with `pip install -r requirements.txt`.
2. Create a `.env` file and populate it with environment variables. You can use multiple `.env` files for different
environments, e.g. `development.env`, `staging.env`. In this case, you need to have a base `.env` file with a specified
`APP_ENV` variable.
3. Run `python main.py`.

## Environment variables (configuration)

`APP_ENV` - an environment where the bot runs, e.g. `development`, `staging`. Default: `development`.  
`BOT_TOKEN` - a Telegram bot token.  
`MAIN_CHAT_ID` - an ID of a main chat, the bot will send greetings there.  
`GIFT_CHAT_ID` - an ID of a chat where users discuss gifts for upcoming birthdays. The user who has a birthday soon will
be banned from this chat.  
`FOLLOWERS_DATA_FILE` - a path to a `.json` file with followers' data. Default: `/data/followers.json`.  
`BIRTHDAYS_DATA_FILE` - a path to a `.json` file with birthdays data, in the format `"iso_date": user_id`.
Default: `/data/birthdays.json`.  
`GIFT_PREP_DAYS` - a number of days users in the gift chat have to make a present. The user who has a birthday in
`GIFT_PREP_DAYS` days or less will be banned. Default: `3`.  
