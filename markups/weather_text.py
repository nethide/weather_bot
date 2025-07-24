async def get_weather_text(weather):
    pressure = int(weather["current"]["pressure_mb"])
    return f"""
☀️ <b>Погода в городе</b> {weather["location"]["name"]}

🍃 <b>Погода:</b> {weather["current"]["condition"]["text"]}
🌏 <b>Страна:</b> {weather["location"]["country"]}

<b>Температура</b> 🌡️
╔🌡️ Температура: {weather["current"]["temp_c"]} C°
╚ℹ️ Ощущается как: {weather["current"]["feelslike_c"]} C°

<b>Ветер</b> 💨
╔⌚ Скорость: {weather["current"]["wind_kph"]} км/ч
╚🧭 Направление: {weather["current"]["wind_dir"]}

🤿 <b>Давление:</b> {pressure}
"""

async def get_weather_text_schedule(weather, date):
    pressure = int(weather["current"]["pressure_mb"])
    return f"""
☀️ <b>Погода на {date}</b> 

🏙️ Город: {weather["location"]["name"]}

🍃 <b>Погода:</b> {weather["current"]["condition"]["text"]}
🌏 <b>Страна:</b> {weather["location"]["country"]}

<b>Температура</b> 🌡️
╔🌡️ Температура: {weather["current"]["temp_c"]} C°
╚ℹ️ Ощущается как: {weather["current"]["feelslike_c"]} C°

<b>Ветер</b> 💨
╔⌚ Скорость: {weather["current"]["wind_kph"]} км/ч
╚🧭 Направление: {weather["current"]["wind_dir"]}

🤿 <b>Давление:</b> {pressure}
"""
