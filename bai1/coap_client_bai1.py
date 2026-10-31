import asyncio

import aiocoap


URI = "coap://127.0.0.1:5683/iot/lab/message"


async def send_request(protocol, method, payload=None):
    request = aiocoap.Message(code=method, uri=URI)

    if payload is not None:
        request.payload = payload.encode("utf-8")

    return await asyncio.wait_for(protocol.request(request).response, timeout=10)


async def main():
    print("CoAP Client")
    name = input("Nhap ho ten sinh vien: ").strip()
    student_id = input("Nhap ma sinh vien: ").strip()

    if not name or not student_id:
        print("Ho ten va ma sinh vien khong duoc de trong")
        return

    protocol = await aiocoap.Context.create_client_context()

    try:
        print("\nSending GET request...")
        print(f"URI: {URI}")

        try:
            response = await send_request(protocol, aiocoap.GET)
            print("\nResponse:")
            print(f"Code: {response.code}")
            print(f"Payload: {response.payload.decode('utf-8')}")
        except Exception as error:
            print(f"GET request failed: {error}")

        message = f"Xin chao tu CoAP Client - {student_id} - {name}"
        print("\nSending POST request...")
        print(f"Payload: {message}")

        try:
            response = await send_request(protocol, aiocoap.POST, message)
            print("\nResponse:")
            print(f"Code: {response.code}")
            print(f"Payload: {response.payload.decode('utf-8')}")
        except Exception as error:
            print(f"POST request failed: {error}")
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient da dung")
    except Exception as error:
        print(f"Loi ket noi: {error}")
