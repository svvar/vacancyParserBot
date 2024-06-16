import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from db import get_by_day
from aiogram.types import BufferedInputFile
import pandas as pd
import datetime
from io import BytesIO

#Key left public for testing purposes
API_TOKEN = '7417246250:AAFPkkmjHUFkym7zaQAMeQeyXkBnPpSA3AY'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("Привіт!")


@dp.message(Command('get_today_statistic'))
async def get_today_statistic(message: types.Message):
    today = datetime.datetime.now()

    today_records = await get_by_day(today.date())
    df = pd.DataFrame({'datetime': [], 'vacancy_count': []})
    for record in today_records:
        df.loc[len(df)] = [record.datetime, record.vacancy_count]

    df['change'] = df['vacancy_count'].diff()
    df['change'] = df['change'].fillna(0)

    with BytesIO() as file:
        with pd.ExcelWriter(file, datetime_format='DD.MM.YYYY HH:MM') as writer:
            df.to_excel(writer, index=False)
        input_file = BufferedInputFile(file.getvalue(), filename=f'statistics {today.strftime("%d.%m.%Y %H:%M")}.xlsx')
        await message.answer_document(document=input_file)


async def start_bot():
    print('Bot startup...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
