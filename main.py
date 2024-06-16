import asyncio
from bot import start_bot
from parser import start_parser

async def main():
    await asyncio.gather(
        start_parser(),
        start_bot(),
    )

if __name__ == '__main__':
    asyncio.run(main())