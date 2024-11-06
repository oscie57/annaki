from game import game_blueprint
import config
import requests
import python_weather

from flask import request
from zoneinfo import ZoneInfo
from datetime import datetime


def pocketcalc(hour:str) -> str:
    
    match hour:
        case "00" | "01" | "02" | "03" | "04" | "22" | "23":
            return "night"
        case "05" | "06" | "07" | "08" | "09" | "10" | "11":
            return "morning"
        case "12" | "13" | "14" | "15" | "16":
            return "day"
        case "17" | "18" | "19" | "20" | "21":
            return "evening"
        case _:
            return "campsite"


def check_server(cloudurl: str) -> tuple[bool, str|dict]:

    try:
        # server is online, return game list
        return True, requests.get(f"{cloudurl}/list.json", timeout=10).json()
    except:
        # server is offline, return error message
        return False, "Could not connect to the server, please try again later."


async def getweather(area: str):
    async with python_weather.Client(format=python_weather.IMPERIAL) as client:
        weather = await client.get(area)

        sky = weather.current.description

        await client.close()

        return sky
    

def get_location() -> tuple[bool, str, str]:

    # get ip address
    if config.DEBUG:
        ip_addr = config.debug_ip
    else:
        ip_addr = request.remote_addr

    url = "http://ip-api.com/json/" + ip_addr

    response = requests.get(url).json()

    if response['status'] == "fail":
        # return error message
        return False, response['message']
    else:
        # return location
        return True, f"{response['city']}, {response['country']}", response['timezone']


@game_blueprint.route('/game/<game>')
async def get_ac(game):
    """Support for AC:NH (NSW), AC:NL (3DS), AC:CF (Wii), AC:PG (GCN), AC:PC (iOS/Android)"""

    cloud_url = config.CLOUD_URL

    server_check = check_server(cloud_url)
    
    # check if server is online
    if server_check[0] == False:
        return server_check[1]

    location = get_location()

    # check if location is valid
    if location[0] == False:
        return location[1]

    weather = await getweather(location[1])

    # get the weather keyword by checking the weather description

    if game == "ac":
        if any(i in weather for i in config.KEYWORDS_SNOW):
            gameweather = "snow"
        else:
            gameweather = "clear"
    else:
        if any(i in weather for i in config.KEYWORDS_SNOW):
            gameweather = "snow"
        elif any(i in weather for i in config.KEYWORDS_RAIN):
            gameweather = "rain"
        else:
            gameweather = "clear"

    # get time and hour while keeping timezone in mind
    gametime = datetime.now(ZoneInfo(location[2]))
    gamehour = gametime.strftime("%H")

    # return the mp3 url
    if game == "acpc":
        return f"{cloud_url}/acpc/{pocketcalc(gamehour)}.mp3"
    else:
        return f"{cloud_url}/{game}/{gameweather}/{gamehour}.mp3"
