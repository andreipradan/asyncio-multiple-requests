import asyncio
from concurrent.futures import ThreadPoolExecutor
from timeit import default_timer

import requests

import settings


def fetch(session, base_url, i):
    start = default_timer()
    with session.get(f"{base_url}&page={i}") as response:
        if response.status_code != 200:
            print(f"FAILURE::STATUS::{response.status_code}::PAGE::{i + 1}")

        elapsed_time = default_timer() - start
        completed_at = "{:5.2f}s".format(elapsed_time)
        print("{0:<30} {1:>20}".format(i + 1, completed_at))
        return response.json()


async def fetch_many(base_url, no_of_pages, callback):
    with ThreadPoolExecutor(max_workers=settings.THREAD_MAX_WORKERS) as executor:
        with requests.Session() as session:
            tasks = [
                asyncio.get_event_loop().run_in_executor(
                    executor,
                    fetch,
                    *(session, base_url, i)
                )
                for i in range(1, no_of_pages + 1)
            ]
            return map(callback, await asyncio.gather(*tasks))
