import requests

from config import OPEN_WEATHER_TOKEN

async def get_weather(city):
    responce = requests.get(
    url="http://api.weatherapi.com/v1/current.json",
    params={
        "key": f"{OPEN_WEATHER_TOKEN}",
        "q": f"{city}",
        "lang": "ru"
    })
    return responce.json()