import asyncio
import json
from datetime import datetime

import aiocoap


URI = "coap://127.0.0.1:5683/iot/lab/sensor01/data"


async def main():
    protocol = await aiocoap.Context.create_client_context()
    print(f"Monitoring Client started: {URI}")

    try:
        while True:
            request = aiocoap.Message(code=aiocoap.GET, uri=URI)

            try:
                response = await asyncio.wait_for(protocol.request(request).response, timeout=5)
                if response.code != aiocoap.CONTENT:
                    print(f"Response Code: {response.code}")
                else:
                    data = json.loads(response.payload.decode("utf-8"))
                    temperature = data["temperature"]
                    humidity = data["humidity"]

                    print(f"\n[{datetime.now():%H:%M:%S}] Received sensor data")
                    print(f"Device: {data['device_id']}")
                    print(f"Temperature: {temperature} C")
                    print(f"Humidity: {humidity} %")

                    if temperature > 35:
                        print("CANH BAO: Nhiet do cao")
                    if humidity < 40:
                        print("CANH BAO: Do am thap")
                    if temperature <= 35 and humidity >= 40:
                        print("Trang thai: Binh thuong")
                    print("-" * 30)
            except Exception as error:
                print(f"Loi khi lay du lieu cam bien: {error}")

            await asyncio.sleep(3)
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDa dung giam sat cam bien")
    except Exception as error:
        print(f"Loi ket noi: {error}")
