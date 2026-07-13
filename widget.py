import json
import os
import requests
import api
from api import searchforchampion, getmastery
from config import config
if os.path.exists(".env"):
    import dotenv
    dotenv.load_dotenv(".env")

discord = {
    "token": str(os.getenv("DISCORD_TOKEN")),
    "appid": int(os.getenv("DISCORD_APP_ID")),
    "uid": int(os.getenv("DISCORD_USER_ID")),
}

data = json.dumps({
  "username": config["discord_user"],
  "data": {
    "dynamic": [
      {
        "type": 1,
        "name": "rank",
        "value": f"{api.getplayerrank()["rank"]}"
      },
      {
        "type": 1,
        "name": "masterypoints",
        "value": f"{api.getmastery()["totalpoints"]}"
      },
      {
        "type": 3,
        "name": "champimage",
        "value": {
          "url": f"{api.searchforchampion(api.gettop1())["image"]}"
        }
      },
      {
        "type": 1,
        "name": "playername",
        "value": f"{config["riotid"]}"
      },
      {
        "type": 1,
        "name": "playerlvl",
        "value": f""
      },
      {
        "type": 1,
        "name": "favchampion",
        "value": f"{api.searchforchampion(api.gettop1())['champion']}"
      },
      {
        "type": 1,
        "name": "region",
        "value": f""
      },
      {
        "type": 1,
        "name": "masterylvl",
        "value": f"{api.getmastery()["masterylvl"]}"
      },
      {
        "type": 1,
        "name": "lp",
        "value": f"{api.getplayerrank()["lp"]}"
      },
      {
        "type": 1,
        "name": "mainmastery",
        "value": f"{api.gettop1()["championPoints"]}"
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
