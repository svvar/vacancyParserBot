import asyncio
import datetime
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import save_request


async def get_vacancy_count():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.rabota.ua/vacancy/search', json={'keywords': 'junior'}) as response:
                return (await response.json())['total']
    except aiohttp.ClientError as e:
        print(e)
        return None


async def scheduled_task():
    count = await get_vacancy_count()
    if count:
        await save_request(count)
        print(datetime.datetime.now(), count)


async def start_parser():
    print('Parser startup...')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_task, 'cron', minute='0')
    scheduler.start()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_parser())
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass