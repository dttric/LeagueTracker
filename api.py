import requests
import json

from config import config as cfg
import os

if os.path.exists(".env"): # универсальное решение против Github Actions ибо там апи ключ уже будет в энве
    import dotenv
    dotenv.load_dotenv()

api_key = os.environ.get("RIOT_API_KEY")
riotid = cfg["riotid"]
gameName, tagLine = riotid.split('#')

def find_parent_by_value(data, target):
    if isinstance(data, dict):
        for key, value in data.items():
            if value == target:
                return data
            result = find_parent_by_value(value, target)
            if result is not None:
                return result

    elif isinstance(data, list):
        for item in data:
            if item == target:
                return data
            result = find_parent_by_value(item, target)
            if result is not None:
                return result

def searchforchampion(champion):
    url = "https://ddragon.leagueoflegends.com/cdn/16.13.1/data/en_US/champion.json"
    request = requests.get(url)
    champlist = request.json()["data"]
    json = find_parent_by_value(champlist, str(champion['championId']))
    return {
        "champion": json['name'],
        "image": f"https://ddragon.leagueoflegends.com/cdn/16.13.1/img/champion/{json['image']['full']}"
    }

def ridtopuuid(riotid):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}"
    request = requests.get(url)
    return request.json()["puuid"]

def gettop1():
    url = f"https://ru.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{ridtopuuid(riotid)}/top?api_key={api_key}"
    request = requests.get(url)
    return {
        "championId": request.json()[0]["championId"],
        "championLevel": request.json()[0]["championLevel"],
        "championPoints": request.json()[0]["championPoints"],
    }

def getmastery():
    url = f"https://ru.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{ridtopuuid(riotid)}?api_key={api_key}"
    request = requests.get(url)
    url2 = f"https://ru.api.riotgames.com/lol/champion-mastery/v4/scores/by-puuid/{ridtopuuid(riotid)}?api_key={api_key}"
    request2 = requests.get(url2)
    totalpoints = 0
    for i in range(len(request.json())):
        totalpoints = totalpoints + int(request.json()[i]["championPoints"])
    return { "totalpoints": totalpoints, "masterylvl": request2.json() }

def getplayerrank():
    url = f"https://ru.api.riotgames.com/lol/league/v4/entries/by-puuid/{ridtopuuid(riotid)}?api_key={api_key}"
    request = requests.get(url)
    match request.json()[0]["tier"]:
        case "IRON": tier = "Железо"
        case "BRONZE": tier = "Бронза"
        case "SILVER": tier = "Серебро"
        case "GOLD": tier = "Золото"
        case "PLATINUM": tier = "Платина"
        case "EMERALD": tier = "Изумруд"
        case "DIAMOND": tier = "Алмаз"
        case "MASTER": tier = "Мастер"
        case "GRANDMASTER": tier = "Грандмастер"
        case "CHALLENGER": tier = "Прентендент"

    return {
        "lp": request.json()[0]["leaguePoints"],
        "rank": f"{tier} " + request.json()[0]["rank"],
        "image": f"https://raw.githubusercontent.com/dttric/LeagueTracker/refs/heads/main/rankedmedals/{str(request.json()[0]["tier"]).lower()}.png"
    }

def getplayer():
    url = f"https://ru.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{ridtopuuid(riotid)}?api_key={api_key}"
    request = requests.get(url)
    return {
        "level": request.json()["summonerLevel"],
        "icon": f"https://ddragon.leagueoflegends.com/cdn/16.13.1/img/profileicon/{request.json()["profileIconId"]}.png"
    }


if __name__ == "__main__":
    print(gettop1())
    print(searchforchampion(gettop1()))
    print(getmastery())
    print(getplayerrank())
    print(getplayer())
