import asyncio
import json
import random

import aiocoap
from aiocoap import resource


class SensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.temperature = 28.5
        self.humidity = 65.2
        self.task = asyncio.create_task(self.update_sensor_data())

    async def update_sensor_data(self):
        while True:
            await asyncio.sleep(3)
            self.temperature = round(random.uniform(20.0, 45.0), 1)
            self.humidity = round(random.uniform(20.0, 90.0), 1)
            print(f"[Sensor Update] Temp: {self.temperature} C, Humidity: {self.humidity} %")

    async def render_get(self, request):
        data = {
            "device_id": "sensor01",
            "temperature": self.temperature,
            "humidity": self.humidity
        }
        print("GET request received for /iot/lab/sensor01/data")
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=json.dumps(data).encode("utf-8"),
            content_format=50
        )


async def main():
    sensor = SensorResource()
    site = resource.Site()
    site.add_resource(["iot", "lab", "sensor01", "data"], sensor)
    server = await aiocoap.Context.create_server_context(site, bind=("127.0.0.1", 5683))

    print("CoAP Sensor Server started on port 5683")
    print("Resource: /iot/lab/sensor01/data")

    try:
        await asyncio.Future()
    finally:
        sensor.task.cancel()
        await asyncio.gather(sensor.task, return_exceptions=True)
        await server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer da dung")
    except Exception as error:
        print(f"Khong the khoi dong Server: {error}")
