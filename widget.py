import json
import os

import requests

# import api
from config import config

# min, max = api.get_progress(config["sid"], config["gid"]).split(":")

discord = {
    "token": os.getenv("DISCORD_TOKEN"),
    "appid": int(os.getenv("DISCORD_APP_ID")),
    "uid": int(os.getenv("DISCORD_USER_ID")),
}

data = json.dumps()

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
