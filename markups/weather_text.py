async def get_weather_text(weather):
    pressure = int(weather["current"]["pressure_mb"])
    return f"""
☀️ <b>Погода в городе</b> {weather["location"]["name"]}
🌏 <b>Страна:</b> {weather["location"]["country"]}

<blockquote>🍃 <b>Погода:</b> {weather["current"]["condition"]["text"]}

<b>Температура 🌡️</b>
ℹ️ На улице {weather["current"]["temp_c"]} C°
<i>*Ощущается как: {weather["current"]["feelslike_c"]} C°</i>

<b>Ветер 💨</b>
⌚ Скорость: {weather["current"]["wind_kph"]} км/ч
🧭 Направление: {weather["current"]["wind_dir"]}

🤿 <b>Давление:</b> {pressure}</blockquote>
"""

async def get_weather_text_schedule(weather, date):
    pressure = int(weather["current"]["pressure_mb"])
    return f"""
☀️ <b>Погода на {date}</b> 
🏙️ Город: {weather["location"]["name"]}
🌏 <b>Страна:</b> {weather["location"]["country"]}

<blockquote>🍃 <b>Погода:</b> {weather["current"]["condition"]["text"]}

<b>Температура 🌡️</b>
ℹ️ На улице {weather["current"]["temp_c"]} C°
<i>*Ощущается как: {weather["current"]["feelslike_c"]} C°</i>

<b>Ветер 💨</b>
⌚ Скорость: {weather["current"]["wind_kph"]} км/ч
🧭 Направление: {weather["current"]["wind_dir"]}

🤿 <b>Давление:</b> {pressure}</blockquote>
"""
