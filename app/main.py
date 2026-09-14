import uasyncio as asyncio
from machine import Pin

MESSAGE = "Hello world from micropy-system-test! HAPPY CODING!"


async def main():
    led = Pin("LED", Pin.OUT)
    print(MESSAGE)
    while True:
        led.toggle()
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
