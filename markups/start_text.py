async def get_start_text():
    return f"""
<b>👋🏻 Привет!</b>

<blockquote>❔ Возможности бота:</blockquote>
--→ Присылает каждый день в заданное время погоду в выбранном городе.

<blockquote>🍃 Начало работы:</blockquote>
--→ Для начала работы введите команду для настройки.
/set [<i>Название города</i>] [<i>Час в 24-х часовом формате</i>]

<blockquote>ℹ️ Пример:</blockquote>
/set Москва 8
<tg-spoiler>by @whitelava</tg-spoiler>
"""