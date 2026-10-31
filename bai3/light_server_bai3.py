import asyncio
import json

import aiocoap
from aiocoap import resource


class LightResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.status = "OFF"
        self.observer_count = 0

    def update_observation_count(self, count):
        if count > self.observer_count:
            print("\nNew Observe registration received")
        self.observer_count = count

    async def render_get(self, request):
        data = {"device_id": "light01", "status": self.status}
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=json.dumps(data).encode("utf-8"),
            content_format=50
        )

    async def render_put(self, request):
        try:
            data = json.loads(request.payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload="Du lieu JSON khong hop le".encode("utf-8")
            )

        if not isinstance(data, dict) or data.get("device_id") != "light01":
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload="Ma thiet bi khong hop le".encode("utf-8")
            )

        command = data.get("command")
        if command not in ("ON", "OFF"):
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload="Lenh dieu khien khong hop le".encode("utf-8")
            )

        print("\nPUT request received:")
        print("Device: light01")
        print(f"Command: {command}")

        if command != self.status:
            old_status = self.status
            self.status = command
            print(f"Light state changed: {old_status} -> {self.status}")
            if self.observer_count:
                print(f"Notify observers: {self.status}")
            self.updated_state()

        message = "Da bat den light01" if command == "ON" else "Da tat den light01"
        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload=message.encode("utf-8")
        )


async def main():
    site = resource.Site()
    site.add_resource(["iot", "lab", "light01", "status"], LightResource())
    server = await aiocoap.Context.create_server_context(site, bind=("127.0.0.1", 5683))

    print("CoAP Smart Light Server started...")
    print("Resource: /iot/lab/light01/status")
    print("Initial status: OFF")

    try:
        await asyncio.Future()
    finally:
        await server.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer da dung")
    except Exception as error:
        print(f"Khong the khoi dong Server: {error}")
