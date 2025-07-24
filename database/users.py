import aiosqlite

async def get_user(telegram_id):
    dp = await aiosqlite.connect("settings.db")
    user = await dp.execute(f"SELECT * FROM settings WHERE telegram_id = {telegram_id}")
    result = await user.fetchone()
    await dp.close()
    return result

async def check_user(telegram_id):
    dp = await aiosqlite.connect("settings.db")
    user = await dp.execute(f"SELECT * FROM settings WHERE telegram_id = {telegram_id}")
    if await user.fetchone() is None:
        await dp.close()
        return False
    else:
        await dp.close()
        return True
    
async def insert_user(telegram_id):
    dp = await aiosqlite.connect("settings.db")
    await dp.execute(f"INSERT INTO settings VALUES({telegram_id}, NULL, NULL, NULL)")
    await dp.commit()
    await dp.close()

async def insert_time(hour, tg_id):
    dp = await aiosqlite.connect("settings.db")
    await dp.execute(f"UPDATE settings SET time = {hour} WHERE telegram_id = {tg_id}")
    await dp.commit()
    await dp.close()

async def add_jobs(job_id, tg_id):
    dp = await aiosqlite.connect("settings.db")
    await dp.execute(f"UPDATE settings SET job_id = '{job_id}' WHERE telegram_id = {tg_id}")
    await dp.commit()
    await dp.close()

async def delete_jobs(tg_id):
    dp = await aiosqlite.connect("settings.db")
    await dp.execute(f"UPDATE settings SET job_id = NULL WHERE telegram_id = {tg_id}")
    await dp.commit()
    await dp.close()