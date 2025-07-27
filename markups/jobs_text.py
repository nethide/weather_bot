async def get_job_text(date, city, utc):
    return f"""
✅ <b> Успешно! </b>

📐 Параметры:
<blockquote>🏙️ Город: {city}
⌚ Время: {date}
🗓️ Часовой пояс: {utc} UTC</blockquote>

ℹ️ <i>Оповещение будет приходить каждый день в указанное время. Поправка на часовой пояс - автоматическая</i>"""