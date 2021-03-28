import asyncio

CONCURRENCY_LIMIT = 6


async def gather_with_concurrency(limit, *tasks, return_exceptions=False):
    """Wrap asyncio.gather to limit the number of concurrent tasks.

    From: https://stackoverflow.com/a/61478547/9127614
    """
    semaphore = asyncio.Semaphore(limit)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(
        *(sem_task(task) for task in tasks), return_exceptions=return_exceptions
    )
