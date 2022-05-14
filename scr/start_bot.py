import asyncio
import telegram
import json

async def main():
    bot = telegram.Bot(json.load(open('../telegram_conf.json', 'r'))['token'])
    async with bot:
        print((await bot.get_updates())[0])


if __name__ == '__main__':
    asyncio.run(main())