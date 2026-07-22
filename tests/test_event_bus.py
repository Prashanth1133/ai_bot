import asyncio

from core.event_bus import EventBus


bus = EventBus()


received = []


async def handler(data):

    received.append(data)


async def test():

    bus.subscribe("trade", handler)

    await bus.publish("trade", 100)

    assert received == [100]


asyncio.run(test())

print("PASS")