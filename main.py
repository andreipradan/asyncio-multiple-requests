import asyncio
from timeit import default_timer

import settings
from backends import aiohttp, requests


def extract_trips(data):
    return sum([item.get('trips') or 0 for item in data['data']])


if __name__ == "__main__":
    url = input(f"Input URL [default: {settings.URL}]: ") or settings.URL
    prompt = """
    Choose request backend [default: aiohttp]:
        [1] aiohttp
        [2] requests
    """
    while (backend := input(prompt)) not in ['1', '2', '']:
        pass

    backend = int(backend or '1')
    pages = input(f'No of pages [default: {settings.NO_OF_PAGES}]: ')
    pages = int(pages) if pages else settings.NO_OF_PAGES

    print("{0:<30} {1:>20}".format("#", "Duration"))  # header

    start = default_timer()
    loop = asyncio.get_event_loop()
    if backend == 1:
        start = default_timer()
        result = loop.run_until_complete(aiohttp.fetch_many(loop, url, pages, extract_trips))
        aiohttp_time = default_timer() - start
        print(" == Aiohttp == ")
        print(f"Total trips: {result}")
        print(f"Duration: {aiohttp_time}s")
    elif backend == 2:
        future = asyncio.ensure_future(requests.fetch_many(url, pages, extract_trips))
        result = loop.run_until_complete(future)
        requests_time = default_timer() - start
        print(" == Requests == ")
        print(f"Total trips: {result}")
        print(f"Duration: {requests_time}s")

    print("Done")
