import json
import os
import requests
import api
from config import config
if os.path.exists(".env"):
    import dotenv
    dotenv.load_dotenv(".env")

discord = {
    "token": os.getenv("DISCORD_TOKEN"),
    "appid": int(os.getenv("DISCORD_APP_ID")),
    "uid": int(os.getenv("DISCORD_USER_ID")),
}

data = json.dumps({
  "data": {
    "dynamic": [
      {
        "type": 1,
        "name": "rank",
        "value": ""
      },
      {
        "type": 1,
        "name": "masterypoints",
        "value": ""
      },
      {
        "type": 3,
        "name": "champimage",
        "value": {
          "url": "<URL to champimage.png>"
        }
      },
      {
        "type": 1,
        "name": "playername",
        "value": ""
      },
      {
        "type": 1,
        "name": "playerlvl",
        "value": ""
      },
      {
        "type": 1,
        "name": "favchampion",
        "value": ""
      },
      {
        "type": 1,
        "name": "region",
        "value": ""
      },
      {
        "type": 1,
        "name": "masterylvl",
        "value": ""
      },
      {
        "type": 1,
        "name": "winrate",
        "value": ""
      },
      {
        "type": 1,
        "name": "mainmastery",
        "value": ""
      }
    ]
  }
})

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bot {discord['token']}",
    "User-Agent": "DiscordBot (https://github.com/discord/discord-api-docs, 1.0.0)",
}

url = f"https://discord.com/api/v9/applications/{discord['appid']}/users/{discord['uid']}/identities/0/profile"

try:
    response = requests.patch(url, headers=headers, data=data)

    if response.status_code in [200, 201, 204]:
        print("✅ Профиль успешно обновлён")
        print(response.json())
    else:
        print(f"❌ Ошибка {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Ошибка подключения: {e}")
