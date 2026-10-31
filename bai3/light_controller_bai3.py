import asyncio
import json

import aiocoap


URI = "coap://127.0.0.1:5683/iot/lab/light01/status"


async def send_request(protocol, method, data=None):
    request = aiocoap.Message(code=method, uri=URI)

    if data is not None:
        request.payload = json.dumps(data).encode("utf-8")
        request.opt.content_format = 50

    return await asyncio.wait_for(protocol.request(request).response, timeout=10)


async def main():
    protocol = await aiocoap.Context.create_client_context()

    try:
        while True:
            command = input("\nNhap lenh (ON/OFF/STATUS/EXIT): ").strip().upper()

            if command == "EXIT":
                print("Da thoat chuong trinh")
                break

            if command not in ("ON", "OFF", "STATUS"):
                print("Lenh khong hop le, vui long nhap lai")
                continue

            try:
                if command == "STATUS":
                    print("\nSending GET request...")
                    response = await send_request(protocol, aiocoap.GET)
                    print(f"Response Code: {response.code}")
                    print(f"Response: {response.payload.decode('utf-8')}")
                else:
                    print("\nSending PUT request...")
                    data = {"device_id": "light01", "command": command}
                    response = await send_request(protocol, aiocoap.PUT, data)
                    print(f"Response Code: {response.code}")
                    print(response.payload.decode("utf-8"))
            except Exception as error:
                print(f"Khong gui duoc yeu cau: {error}")
    finally:
        await protocol.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nController da dung")
    except Exception as error:
        print(f"Loi ket noi: {error}")
