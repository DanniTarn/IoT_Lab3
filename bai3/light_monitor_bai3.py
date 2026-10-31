import asyncio
import json
from datetime import datetime

import aiocoap


URI = "coap://127.0.0.1:5683/iot/lab/light01/status"


def show_status(response, title):
    data = json.loads(response.payload.decode("utf-8"))
    print(f"\n[{datetime.now():%H:%M:%S}] {title}")
    print(f"Device: {data['device_id']}")
    print(f"Status: {data['status']}")


async def main():
    protocol = await aiocoap.Context.create_client_context()
    observation = None

    try:
        print("Registering CoAP Observe...")
        request = aiocoap.Message(code=aiocoap.GET, uri=URI, observe=0)
        pending = protocol.request(request)
        response = await asyncio.wait_for(pending.response, timeout=10)

        if response.opt.observe is None or pending.observation is None:
            print("Server khong ho tro Observe")
            return

        observation = pending.observation
        print("Observe registration successful")
        show_status(response, "Initial State")

        async for response in observation:
            show_status(response, "State Updated")
    finally:
        if observation is not None:
            observation.cancel()
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDa dung theo doi trang thai den")
    except Exception as error:
        print(f"Loi giam sat: {error}")
