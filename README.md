# Secret Santa Bot

## Overview

This a simple bot for Secret Santa. The bot randomly assigns participants and privately messages them on discord about their assigned gift recipient.

## Features

- **Organiser Exclusive:** The `secretsanta` command can only be used by the organiser.
- **Rules** You can set a list of rules and a budget.

## Commands

`!help`: This will bring up the help menu.

`!rules`: This will bring up a list of rules and the budget.

`!secretsanta`: This will assign who's buying for who.

## Example Santa Config

```json
{
    "organiser_discord_username": "ronan#0",
    "rules": {
        "budget": 25,
        "rules_list": [
            "No super expensive gifts",
            "No gift cards"
        ]
    },
    "participants": [
        {
            "name": "Ronan",
            "discord_user_id": "338728782837883383",
            "address": "1 Main St, City, Country"
        },
        {
            "name": "Joe",
            "discord_user_id": "2983877476736797288",
            "address": "123 Main St, City, Country"
        },
        {
            "name": "Bob",
            "discord_user_id": "3948928478372783733",
            "address": "456 Oak Ave, Town, Country"
        },
        {
            "name": "Bill",
            "discord_user_id": "1009299847574673773",
            "address": "789 Elm Blvd, Village, Country"
        },
    ]
}
```

## Setup

1. Clone the repo

2. Install required libraries and packages

```bash
pip install -r requirements.txt
```

3. Create a `santa_config.json`. You can just edit the example one above.
   
4. Create a `.env` file with your bot token
```env
TOKEN=<your bot token>
```