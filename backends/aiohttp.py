import asyncio
from timeit import default_timer

import aiohttp

import settings


async def fetch(session, sem, url, i):
    start = default_timer()
    async with sem:
        async with session.get(f"{url}&page={i}") as response:
            if response.status != 200:
                print(f"FAILURE::STATUS::{response.status_code}::PAGE::{i}")
            elapsed_time = default_timer() - start
            completed_at = "{:5.2f}s".format(elapsed_time)
            print("{0:<30} {1:>20}".format(i, completed_at))
            return await response.json()


async def fetch_many(loop, url, pages, callback):
    sem = asyncio.Semaphore(settings.SEMAPHORE_VALUE)
    async with aiohttp.ClientSession(loop=loop) as session:
        return map(callback, await asyncio.gather(
            *[fetch(session, sem, url, i) for i in range(1, pages + 1)]
        ))
