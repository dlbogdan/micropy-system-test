import uasyncio as asyncio
from machine import Pin

MESSAGE = "Starting intentionally hung watchdog candidate 1.0.23"


async def main():
    led = Pin("LED", Pin.OUT)
    print(MESSAGE)
    # Deliberately remain responsive to the event loop without confirming.
    # Stable watchdog infrastructure must stop feeding after its candidate
    # deadline, reset the device, and let the launcher roll this release back.
    while True:
        led.toggle()
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
