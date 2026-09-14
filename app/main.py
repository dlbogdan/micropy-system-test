import uasyncio as asyncio
from machine import Pin
from lib.coresys.ota_state import load_state
from lib.coresys.slot_manager import confirm_running_slot

MESSAGE = "Hello from A/B-only Milestone 4 candidate 1.0.24"


async def main():
    led = Pin("LED", Pin.OUT)
    print(MESSAGE)
    await asyncio.sleep(3)
    state = load_state()
    running_slot = state["pending"] or state["active"]
    confirm_running_slot(running_slot)
    print("Confirmed healthy application slot: " + running_slot)
    while True:
        led.toggle()
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
