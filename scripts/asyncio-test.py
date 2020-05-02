import asyncio


async def coroutine1():
    print('c11')
    await asyncio.sleep(1)
    print('c12')
    await asyncio.sleep(1)
    print('c13')
    await asyncio.sleep(1)


async def coroutine2():
    c1 = coroutine1()
    print('c21')
    await c1


async def coroutine3():
    t1 = asyncio.create_task(coroutine1())
    t2 = asyncio.create_task(coroutine1())
    t3 = asyncio.create_task(coroutine1())
    print('c31')
    await t1
    print('c32')
    await t2
    print('c33')
    await t3


asyncio.run(coroutine2())
asyncio.run(coroutine3())
