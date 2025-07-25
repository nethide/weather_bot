async def get_weather_error():
    return f"""
<b>⚠ ️Ошибка синтаксиса!</b>
 
ℹ️ Используйте set вот так:
<blockquote>/set [город] [время]</blockquote>
<i>*Принимаются только целые числа от 0 до 23</i>"""

async def get_weather_error2():
    return f"""
<b>⚠ ️Ошибка синтаксиса!</b>

ℹ️ Используйте weather вот так:
<blockquote>/weather [город]</blockquote>"""