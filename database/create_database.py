import aiosqlite

async def create_database():
    dp = await aiosqlite.connect("settings.db")
    await dp.execute("""CREATE TABLE IF NOT EXISTS settings(telegram_id INTEGER,
                                                    city TEXT,
                                                    time TEXT,
                                                    job_id TEXT)""")
    await dp.close()


