import asyncio
from datetime import datetime

import aiocoap
from aiocoap import resource


class MessageResource(resource.Resource):
    async def render_get(self, request):
        print("GET request received: /iot/lab/message")
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload="Xin chao tu CoAP Server".encode("utf-8")
        )

    async def render_post(self, request):
        try:
            message = request.payload.decode("utf-8")
        except UnicodeDecodeError:
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload="Thong diep khong hop le".encode("utf-8")
            )

        if not message.strip():
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload="Thong diep khong duoc de trong".encode("utf-8")
            )

        print("\nPOST request received:")
        print(f"Payload: {message}")
        print(f"Time: {datetime.now():%H:%M:%S}")

        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload="Server da nhan thong diep".encode("utf-8")
        )


async def main():
    site = resource.Site()
    site.add_resource(["iot", "lab", "message"], MessageResource())
    server = await aiocoap.Context.create_server_context(site, bind=("127.0.0.1", 5683))

    print("CoAP Server started on port 5683")
    print("Resource: coap://127.0.0.1:5683/iot/lab/message")

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
