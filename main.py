import asyncio
import uvloop
import time

from aiowikibot import Bot

async def main():
    bot = Bot(username, password, api_url)
    await bot.login_wiki()
    
    tasks = []
    for i in range(100):
        tasks.append(bot.write_wiki(title, text, desc))
    results = await asyncio.gather(*tasks)
    #print(results)
    #for result in results:
        #print(result)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    start = time.perf_counter()
    loop.run_until_complete(main())
    end = time.perf_counter()
    print(f"用时{end - start}s")