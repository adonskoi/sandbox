import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

import httpx
from memory_profiler import profile


execution_times = []


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        execution_times.append(f"{func.__name__} took {end - start} seconds")
        return result
    return wrapper


def sync_fetch(i: str) -> None:
    resp = httpx.get("https://google.com?search=python" + i)
    resp2 = httpx.get("https://yandex.ru")
    resp.text[:10]
    resp2.text[:10]
    resp3 = httpx.get("https://google.com?search=python" + i)
    resp3.text[:10]
    time.sleep(.2)


async def async_fetch(i: str) -> None:
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://google.com?search=python" + i)
        resp2 = await client.get("https://yandex.ru")
        resp.text[:10]
        resp2.text[:10]
        resp3 = await client.get("https://google.com?search=python" + i)
        resp3.text[:10]
        await asyncio.sleep(.2)


@timeit
@profile
def run_sync(n: int) -> None:
    for i in range(n):
        sync_fetch(str(i))
    print("done sync")


@timeit
@profile
def run_sync_parallel(n: int, max_workers: int = 10) -> None:
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(n):
            executor.submit(sync_fetch, str(i))
    print("done sync parallel")


@timeit
@profile
async def run_async(n: int) -> None:
    tasks = []
    for i in range(n):
        tasks.append(async_fetch(str(i)))
    await asyncio.gather(*tasks)
    print("done async")


if __name__ == "__main__":
    n = 30
    print(f"Running sync with {n} requests")
    run_sync(n)
    asyncio.run(run_async(n))
    run_sync_parallel(n)
    run_sync_parallel(n, max_workers=n)

    for time in execution_times:
        print(time)
