import asyncio

from core.event_bus import EventBus


bus = EventBus()


received = []


async def handler(data):

    received.append(data)


async def _run():

    bus.subscribe("trade", handler)

    await bus.publish("trade", 100)

    assert received == [100]


def test_event_bus():
    received.clear()
    asyncio.run(_run())
